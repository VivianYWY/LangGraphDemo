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

# 2. 初始化 LLM（使用 OpenAI 的 GPT-3.5/4）
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 3. 定义工作流节点函数
def check_tool_need(state: AssistantState) -> AssistantState:
    """
    节点1：判断是否需要调用工具
    """
    query = state["user_query"]
    # 简单判断：包含"天气"关键词则需要调用工具
    # 实际场景中可以用 LLM 来智能判断
    if "天气" in query:
        state["tool_needed"] = True
    else:
        state["tool_needed"] = False
    return state


def generate_answer(state: AssistantState) -> AssistantState:
    """
    节点3：生成最终回答
    """
    query = state["user_query"]
    if state["tool_needed"]:
        # 使用工具结果生成回答
        state["final_answer"] = f"根据查询结果：{state['tool_result']}"
    else:
        # 直接回答通用问题
        response = llm.invoke([HumanMessage(content=query)])
        state["final_answer"] = response.content
    return state

# 4. 构建 LangGraph 工作流
def create_assistant_graph():
    # 创建状态图
    graph = StateGraph(AssistantState)

    # 添加节点
    graph.add_node("check_tool_need", check_tool_need)  # 检查是否需要工具
    graph.add_node("call_weather_tool", call_weather_tool)  # 调用天气工具
    graph.add_node("generate_answer", generate_answer)  # 生成回答

    # 设置入口点
    graph.set_entry_point("check_tool_need")

    # 添加条件边：根据是否需要工具决定下一步
    def tool_branch(state: AssistantState) -> str:
        if state["tool_needed"]:
            return "call_weather_tool"
        else:
            return "generate_answer"

    graph.add_conditional_edges(
        "check_tool_need",
        tool_branch,
        {
            "call_weather_tool": "call_weather_tool",
            "generate_answer": "generate_answer"
        }
    )

    # 添加普通边：工具调用完成后生成回答
    graph.add_edge("call_weather_tool", "generate_answer")

    # 生成回答后结束
    graph.add_edge("generate_answer", END)

    # 编译图
    return graph.compile()
