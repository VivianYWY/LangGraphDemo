from fastapi import FastAPI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any
import asyncio

class AgentState(TypedDict):
    question: str
    result: Any
    
# LangGraph 节点
async def agent_node(state: AgentState):
    # 这里是 MCP 调用逻辑
    result = await call_mcp_tool(state["question"])
    return {"result": result}

# 构建 Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
graph = workflow.compile()
