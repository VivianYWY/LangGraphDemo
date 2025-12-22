  
from typing import Annotated, Sequence, TypedDict  
from langchain\_core.messages import AnyMessage, SystemMessage  
from langgraph.graph.message import add\_messages  
  
class SubAgentState(TypedDict):  
    messages: Annotated[Sequence[AnyMessage], add\_messages]
