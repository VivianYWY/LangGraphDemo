from typing import Dict, List, TypedDict, Any, Optional
import json
import os
from dotenv import load_dotenv
# Modern imports for langchain and langgraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
# Load environment variables
load_dotenv()
