from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import operator

# 定义工作流状态
class WorkflowState(TypedDict):
    input: str
    result: Annotated[str, operator.add]  # 用于字符串累积拼接

# 定义节点函数
def node_a(state: WorkflowState) -> dict:
    processed_result = state['input'].upper()
    return {"result": f"节点A处理: {processed_result}\n"}

def node_b(state: WorkflowState) -> dict:
    return {"result": "节点B处理: 完成\n"}

# 构建工作流
workflow = StateGraph(WorkflowState)
workflow.add_node("node_a", node_a)
workflow.add_node("node_b", node_b)
