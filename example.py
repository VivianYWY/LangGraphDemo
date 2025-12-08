from IPython.display import Image, display
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from typing_extensions import TypedDict


# 4. 运行Graph工作流
def run_workflow():
    """运行"把大象装冰箱"的工作流"""
    # 构建图
    graph = build_graph()
    # 定义初始状态
    initial_state = ElephantInFridgeState(fridge_open=False, elephant_inside=False)
    # 运行图
    result = graph.invoke(initial_state)
    # 输出最终状态
    print("\n工作流执行完毕，最终状态:")
    print(f"冰箱门状态: {'打开' if result["fridge_open"] else '关闭'}")
    print(f"大象是否在冰箱内: {'是' if result["elephant_inside"] else '否'}")
    # 可视化工作流图
    display(Image(graph.get_graph().draw_mermaid_png()))
    return result

# 执行入口
if __name__ == "__main__":
    final_state = run_workflow()