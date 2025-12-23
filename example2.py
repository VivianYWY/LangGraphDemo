  
from typing import Annotated, Sequence, TypedDict  
from langchain\_core.messages import AnyMessage, SystemMessage  
from langgraph.graph.message import add\_messages  
  
class SubAgentState(TypedDict):  
    messages: Annotated[Sequence[AnyMessage], add\_messages]


from dotenv import load\_dotenv  
load\_dotenv()  
  
from langchain.chat\_models import init\_chat\_model  
llm = init\_chat\_model("deepseek-chat", model\_provider="deepseek")
