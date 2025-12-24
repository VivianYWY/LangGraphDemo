  
from typing import Annotated, Sequence, TypedDict  
from langchain\_core.messages import AnyMessage, SystemMessage  
from langgraph.graph.message import add\_messages  
  
class SubAgentState(TypedDict):  
    messages: Annotated[Sequence[AnyMessage], add\_messages]


from dotenv import load\_dotenv  
load\_dotenv()  
  
from langchain.chat\_models import init\_chat\_model  
llm = init\_chat\_model("deepseek-chat", model\_provider="deepseek")



from langchain\_core.tools import tool  
from datetime import datetime  
  
@tool  
def get\_current\_time() -> str:  
    """获取当前的日期和时间，返回格式化的时间字符串。当用户询问时间相关问题时使用此工具。"""  
    now = datetime.now()  
    # 格式化日期和时间  
    date\_str = now.strftime("%Y年%m月%d日")  
    time\_str = now.strftime("%H:%M:%S")  
    # 获取星期几  
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]  
    weekday\_str = weekdays[now.weekday()]  
    # 判断上午/下午  
    hour = now.hour  
    if hour < 12:  
        period = "上午"  
    elif hour < 18:  
        period = "下午"  
    else:  
        period = "晚上"  
    # 返回友好的时间描述  
    return f"当前时间是：{date\_str} {weekday\_str} {period} {time\_str}"
