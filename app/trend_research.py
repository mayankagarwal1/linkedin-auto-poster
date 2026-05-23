import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

SEARCH_QUERIES = [
    "latest LangGraph updates and state management",
    "Model Context Protocol (MCP) AI tools adoption",
    "recent autonomous AI agent frameworks",
    "production RAG architecture trends",
    "OpenAI Agents SDK production use cases"
]

def get_trends() -> str:
    """Scrapes recent data to feed the Analyst Agent."""
    all_results = []

    for query in SEARCH_QUERIES:
        try:
            response = client.search(
                query=query,
                search_depth="basic", # Basic is faster for trend aggregation
                max_results=2
            )

            for item in response.get("results", []):
                all_results.append(
                    f"Trend Query: {query}\n"
                    f"Title: {item.get('title')}\n"
                    f"Summary: {item.get('content')}\n"
                )
        except Exception as e:
            print(f"Error fetching trends for '{query}': {e}")
            continue

    return "\n".join(all_results)