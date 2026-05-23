from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def tavily_search(query: str) -> str:
    """Search latest AI/tech news from web using Tavily."""

    response = client.search(
        query=query,
        topic="general",
        search_depth="advanced",
        max_results=5,
        include_answer=True
    )

    snippets = []

    if response.get("answer"):
        snippets.append(response["answer"])

    for item in response["results"]:
        snippets.append(item["content"])

    return "\n".join(snippets)