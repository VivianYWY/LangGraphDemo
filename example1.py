# 配置内存持久化（生产环境可改用Redis等分布式存储）
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 编译工作流
app = workflow.compile(checkpointer=checkpointer)

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
