from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.config import llm
from app.prompt import ANALYST_PROMPT, WRITER_PROMPT, REVIEW_PROMPT
from app.trend_research import get_trends
from app.tavily_client import research_topic
from app.saver import save_post

# 1. Define the State
class PostState(TypedDict):
    selected_topic: str
    research: str
    draft: str
    final_post: str
    file_path: str

# 2. Define the Nodes
def analyst_node(state: PostState):
    trends = get_trends()
    prompt = ANALYST_PROMPT.format(research=trends)
    result = llm.invoke(prompt)
    return {"selected_topic": result.content.strip()}

def research_node(state: PostState):
    research_data = research_topic(state["selected_topic"])
    return {"research": research_data}

def writer_node(state: PostState):
    prompt = WRITER_PROMPT.format(
        topic=state["selected_topic"],
        research=state["research"]
    )
    result = llm.invoke(prompt)
    return {"draft": result.content}

def reviewer_node(state: PostState):
    prompt = REVIEW_PROMPT.format(draft=state["draft"])
    result = llm.invoke(prompt)
    return {"final_post": result.content}

def save_node(state: PostState):
    file_path = save_post(
        state["selected_topic"],
        state["final_post"]
    )
    return {"file_path": file_path}

# 3. Build the Graph
builder = StateGraph(PostState)

builder.add_node("analyst", analyst_node)
builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_node("review", reviewer_node)
builder.add_node("save", save_node)

builder.set_entry_point("analyst")

builder.add_edge("analyst", "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", "review")
builder.add_edge("review", "save")
builder.add_edge("save", END)

# Compile
graph = builder.compile()