import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def research_topic(topic: str) -> str:
    """Perform a deep search on a specific technical topic."""
    try:
        response = tavily_client.search(
            query=topic,
            search_depth="advanced",
            max_results=5
        )

        results = []
        for item in response.get("results", []):
            results.append(
                f"Title: {item.get('title')}\n"
                f"Content: {item.get('content')}\n"
                f"URL: {item.get('url')}\n"
            )

        return "\n".join(results)
    except Exception as e:
        print(f"Error researching topic '{topic}': {e}")
        return "Research unavailable due to an API error."