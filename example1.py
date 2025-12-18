from langgraph.graph import StateGraph, START, END

# 初始化状态图
workflow = StateGraph(RiskControlState)

# 添加节点
workflow.add_node("planner", planner_agent)
workflow.add_node("data_collector", data_collector_agent)
workflow.add_node("analyzer", analyzer_agent)
workflow.add_node("audit", audit_agent)

# 定义线性流转路径
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "data_collector")
workflow.add_edge("data_collector", "analyzer")
workflow.add_edge("analyzer", "audit")

def route_audit(state: RiskControlState):
    """根据审核结果决定下一步流程"""
    return "human_audit" if state["need_human_audit"] else END

# 添加人工审核节点
workflow.add_node("human_audit", human_audit_agent)

# 定义条件分支
workflow.add_conditional_edges(
    "audit",  # 源节点
    route_audit,  # 路由判断函数
    {
        "human_audit": "human_audit",  # 高风险路径
        END: END  # 低风险路径
    }
)

# 人工审核后流程闭环
workflow.add_edge("human_audit", END)


# 配置内存持久化（生产环境可改用Redis等分布式存储）
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 编译工作流
app = workflow.compile(checkpointer=checkpointer)


# 添加并行处理节点
workflow.add_node("sentiment_analyzer", sentiment_agent)  # 市场情绪分析
workflow.add_node("news_monitor", news_agent)  # 相关新闻监控

# 数据采集后并行执行两个子任务
workflow.add_edge("data_collector", ["sentiment_analyzer", "news_monitor"])

# 并行任务完成后汇总到分析节点
workflow.add_edge("sentiment_analyzer", "analyzer")
workflow.add_edge("news_monitor", "analyzer")


# 执行工作流
def run_risk_control(user_query: str, stock_code: str):
    initial_state = {
        "user_query": user_query,
        "stock_code": stock_code,
        "real_time_data": {},
        "risk_indicators": [],
        "analysis_report": "",
        "audit_result": None,
        "current_agent": "",
        "messages": []
    }
    # 流式执行并返回结果
    result = app.invoke(initial_state)
    return result["analysis_report"]
