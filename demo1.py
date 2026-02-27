from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any
import asyncio

class AgentState(TypedDict):
    question: str
    result: Any
