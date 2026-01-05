import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import HumanMessage, AIMessage

# 加载环境变量（请确保你的 .env 文件中有 OPENAI_API_KEY）
load_dotenv()

# 1. 定义状态结构：整个工作流中共享的数据
class AssistantState(TypedDict):
    """定义工作流的状态结构"""
    user_query: str  # 用户的原始问题
    tool_needed: bool  # 是否需要调用工具
    tool_result: str  # 工具调用的结果
    final_answer: str  # 最终回答
