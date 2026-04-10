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

# 建立连接
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", "END")

# 编译并执行
app = workflow.compile()
result = app.invoke({"input": "hello world"})
print(result)

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 定义工作流状态
class AgentState(TypedDict):
    input: str
    is_too_short: bool

# 定义节点函数
def entry_node(state: AgentState) -> dict:
    if len(state['input']) < 10:
        return {"is_too_short": True}
    return {"is_too_short": False}

def fix_node(state: AgentState) -> dict:
    new_input = state['input'] + "（已修正）"
    return {"input": new_input, "is_too_short": False}

# 定义条件分支逻辑
def should_continue(state: AgentState):
    return "fix_node" if state["is_too_short"] else END

# 构建工作流
workflow = StateGraph(AgentState)
workflow.add_node("entry_node", entry_node)
workflow.add_node("fix_node", fix_node)

# 建立连接
workflow.set_entry_point("entry_node")
workflow.add_edge("fix_node", "entry_node")  # 形成循环
workflow.add_conditional_edges(
    "entry_node",
    should_continue,
    {"fix_node": "fix_node", END: END}
)

# 编译工作流
app = workflow.compile()
