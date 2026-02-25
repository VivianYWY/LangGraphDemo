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

RESEARCHER_SYSTEM_PROMPT = """
You are a skilled research agent tasked with gathering comprehensive information on a given topic. 
Your responsibilities include:
1. Analyzing the research query to understand what information is needed
2. Conducting thorough research to collect relevant facts, data, and perspectives
3. Organizing information in a clear, structured format
4. Ensuring accuracy and objectivity in your findings
5. Citing sources or noting where information might need verification
6. Identifying potential gaps in the information
Present your findings in a well-structured format with clear sections and bullet points where appropriate.
Your goal is to provide comprehensive, accurate, and useful information that fully addresses the research query.
"""

def create_researcher_agent(model="gpt-4o", temperature=0.7):
    """Create a researcher agent using the specified LLM."""
    # Initialize the model
    llm = ChatOpenAI(model=model, temperature=temperature)
    def researcher_function(messages):
        """Function that processes messages and returns a response from the researcher agent."""
        # Add the system prompt if it's not already there
        if not messages or not isinstance(messages[0], SystemMessage) or messages[0].content != RESEARCHER_SYSTEM_PROMPT:
            messages = [SystemMessage(content=RESEARCHER_SYSTEM_PROMPT)] + (messages if isinstance(messages, list) else [])
        # Get response from the LLM
        response = llm.invoke(messages)
        return response
    return researcher_function


# Define the state type for our research workflow
class ResearchState(TypedDict):
    """Type definition for our research workflow state."""
    messages: List[BaseMessage]  # The conversation history
    query: str  # The research query
    research: Optional[str]  # The research findings
    next: Optional[str]  # Where to go next in the graph

def researcher_node(state: ResearchState) -> ResearchState:
    """A node in our graph that performs research on the query."""
    # Get the query from the state
    query = state["query"]
    # Create a message specifically for the researcher
    research_message = HumanMessage(content=f"Please research the following topic thoroughly: {query}")
    # Get the researcher agent
    researcher = create_researcher_agent()
    # Get response from the researcher agent
    response = researcher([research_message])
    # Update the state with the research findings
    new_messages = state["messages"] + [research_message, response]
    # Return the updated state
    return {
        **state,
        "messages": new_messages,
        "research": response.content,
        "next": "output"  # In a multi-agent system, this would go to the next agent
    }

def build_research_graph():
    """Build a simple research workflow using LangGraph."""
    # Create a new graph with our state type
    workflow = StateGraph(ResearchState)
    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("output", output_node)
    # Add edges
    workflow.add_edge("researcher", "output")
    # Set the entry point
    workflow.set_entry_point("researcher")
    # Compile the graph
    return workflow.compile()

ENHANCED_RESEARCHER_PROMPT = """
You are a skilled research agent tasked with gathering comprehensive information on a given topic. 
Your responsibilities include:
1. Analyzing the research query to understand what information is needed
2. Conducting thorough research to collect relevant facts, data, and perspectives
3. Organizing information in a clear, structured format
4. Ensuring accuracy and objectivity in your findings
5. Citing sources or noting where information might need verification
6. Identifying potential gaps in the information
Present your findings in the following structured format:
SUMMARY: A brief overview of your findings (2-3 sentences)
KEY POINTS:
- Point 1
- Point 2
- Point 3
DETAILED FINDINGS:
1. [Topic Area 1]
   - Details and explanations
   - Supporting evidence
   - Different perspectives if applicable
2. [Topic Area 2]
   - Details and explanations
   - Supporting evidence
   - Different perspectives if applicable
GAPS AND LIMITATIONS:
- Identify any areas where information might be incomplete
- Note any contradictions or areas of debate
- Suggest additional research that might be needed
Your goal is to provide comprehensive, accurate, and useful information that fully addresses the research query.
"""

class EnhancedResearchState(TypedDict):
    """Enhanced type definition for our research workflow state."""
    messages: List[BaseMessage]
    query: str
    structured_research: Optional[str]
    next: Optional[str]

CRITIC_SYSTEM_PROMPT = """
You are a Critic Agent, part of a collaborative research assistant system. Your role is to evaluate 
and challenge information provided by the Researcher Agent to ensure accuracy, completeness, and objectivity.
Your responsibilities include:
1. Analyzing research findings for accuracy, completeness, and potential biases
2. Identifying gaps in the information or logical inconsistencies
3. Asking important questions that might have been overlooked
4. Suggesting improvements or alternative perspectives
5. Ensuring that the final information is balanced and well-rounded
Be constructive in your criticism. Your goal is not to dismiss the researcher's work, but to strengthen it.
Format your feedback in a clear, organized manner, highlighting specific points that need attention.
Remember, your ultimate goal is to ensure that the final research output is of the highest quality possible.
"""

class CollaborativeResearchState(TypedDict):
    """State type for our collaborative research assistant."""
    messages: List[BaseMessage]  # The conversation history
    next: Optional[str]  # Where to go next in the graph

def build_collaborative_research_assistant():
    """Build a collaborative research assistant with researcher and critic agents."""
    # Create a new graph with our state type
    workflow = StateGraph(CollaborativeResearchState)
    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("output", output_node)
    # Add edges
    workflow.add_edge("researcher", "critic")
    workflow.add_edge("critic", "output")
    # Set the entry point
    workflow.set_entry_point("researcher")
    # Compile the graph
    return workflow.compile()

class CriticEvaluation(BaseModel):
    """Structured format for critic evaluations."""
    quality_score: int = Field(description="Overall quality score from 1-10")
    strengths: List[str] = Field(description="Key strengths of the research")
    areas_for_improvement: List[str] = Field(description="Areas that need improvement")
    missing_information: List[str] = Field(description="Important information that was not included")
    bias_assessment: str = Field(description="Assessment of potential biases in the research")
    additional_questions: List[str] = Field(description="Questions that should be addressed")

WRITER_SYSTEM_PROMPT = """
You are a Writer Agent, part of a collaborative research assistant system. Your role is to synthesize 
information from the Researcher Agent and feedback from the Critic Agent into a coherent, well-written response.
Your responsibilities include:
1. Analyzing the information provided by the researcher and the feedback from the critic
2. Organizing the information in a logical, easy-to-understand structure
3. Presenting the information in a clear, engaging writing style
4. Balancing different perspectives and ensuring objectivity
5. Creating a final response that is comprehensive, accurate, and well-written
Format your response in a clear, organized manner with appropriate headings, paragraphs, and bullet points.
Use simple language to explain complex concepts, and provide examples where helpful.
Remember, your goal is to create a final response that effectively communicates the information to the user.
"""

class CollaborativeResearchState(TypedDict):
    """State type for our collaborative research assistant."""
    messages: List[BaseMessage]  # The conversation history
    next: Optional[str]  # Where to go next in the graph


def build_collaborative_research_assistant():
    """Build a collaborative research assistant with researcher and critic agents."""
    # Create a new graph with our state type
    workflow = StateGraph(CollaborativeResearchState)
    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("output", output_node)
    # Add edges
    workflow.add_edge("researcher", "critic")
    workflow.add_edge("critic", "output")
    # Set the entry point
    workflow.set_entry_point("researcher")
    # Compile the graph
    return workflow.compile()

class CriticEvaluation(BaseModel):
    """Structured format for critic evaluations."""
    quality_score: int = Field(description="Overall quality score from 1-10")
    strengths: List[str] = Field(description="Key strengths of the research")
    areas_for_improvement: List[str] = Field(description="Areas that need improvement")
    missing_information: List[str] = Field(description="Important information that was not included")
    bias_assessment: str = Field(description="Assessment of potential biases in the research")
    additional_questions: List[str] = Field(description="Questions that should be addressed")

WRITER_SYSTEM_PROMPT = """
You are a Writer Agent, part of a collaborative research assistant system. Your role is to synthesize 
information from the Researcher Agent and feedback from the Critic Agent into a coherent, well-written response.
Your responsibilities include:
1. Analyzing the information provided by the researcher and the feedback from the critic
2. Organizing the information in a logical, easy-to-understand structure
3. Presenting the information in a clear, engaging writing style
4. Balancing different perspectives and ensuring objectivity
5. Creating a final response that is comprehensive, accurate, and well-written
Format your response in a clear, organized manner with appropriate headings, paragraphs, and bullet points.
Use simple language to explain complex concepts, and provide examples where helpful.
Remember, your goal is to create a final response that effectively communicates the information to the user.
"""

class CollaborativeResearchState(TypedDict):
    """State type for our collaborative research assistant."""
    messages: List[BaseMessage]  # The conversation history
    next: Optional[str]  # Where to go next in the graph

def writer_node(state: CollaborativeResearchState) -> CollaborativeResearchState:
    """Node function for the writer agent."""
    # Extract messages from the state
    messages = state["messages"]
    # Create writer messages with the system prompt
    writer_messages = [SystemMessage(content=WRITER_SYSTEM_PROMPT)] + messages
    # Initialize the LLM with a balance of creativity and accuracy
    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
    # Get the writer's response
    response = llm.invoke(writer_messages)
    # Return the updated state
    return {
        "messages": messages + [response],
        "next": "output"
    }

def build_complete_research_assistant():
    """Build a complete research assistant with researcher, critic, and writer agents."""
    # Create a new graph with our state type
    workflow = StateGraph(CollaborativeResearchState)
    # Add nodes
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("output", output_node)
    # Add edges
    workflow.add_edge("researcher", "critic")
    workflow.add_edge("critic", "writer")
    workflow.add_edge("writer", "output")
    # Set the entry point
    workflow.set_entry_point("researcher")
    # Compile the graph
    return workflow.compile()

class EnhancedResearchState(TypedDict):
    """Enhanced state type with metadata for the research process."""
    messages: List[BaseMessage]  # The conversation history
    metadata: Dict[str, Any]  # Metadata about each step in the process
    next: Optional[str]  # Where to go next in the graph

def coordinator_node(state: ResearchState) -> ResearchState:
    """Coordinator node that decides the workflow path."""
    # Extract messages from the state
    messages = state["messages"]
    # Create coordinator messages with the system prompt
    coordinator_messages = [SystemMessage(content=COORDINATOR_SYSTEM_PROMPT)] + messages
    # Initialize the LLM with a lower temperature for consistent decision-making
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
    # Get the coordinator's response
    response = llm.invoke(coordinator_messages)
    # Parse the JSON response to determine next steps
    try:
        decision = json.loads(response.content)
        next_step = decision.get("next", "researcher")  # Default to researcher if not specified
    except Exception:
        # If there's an error parsing the JSON, default to the researcher
        next_step = "researcher"
    # Return the updated state
    return {"messages": messages, "next": next_step}

# Add conditional edges from the coordinator
workflow.add_conditional_edges(
    "coordinator",
    lambda state: state["next"],
    {
        "researcher": "researcher",
        "done": "output"
    }
)
def build_dynamic_research_assistant():
    """Build a dynamic research assistant with a coordinator agent managing the workflow."""
    # Create a new graph
    workflow = Graph()

    # Add nodes
    workflow.add_node("coordinator", coordinator_agent)
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("critic", critic_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("output", output)

    # Add conditional edges from the coordinator
    workflow.add_conditional_edges(
        "coordinator",
        lambda state: state["next"],
        {
            "researcher": "researcher",
            "done": "output"
        }
    )

    # Add the rest of the edges
    workflow.add_edge("researcher", "critic")
    workflow.add_edge("critic", "writer")
    workflow.add_edge("writer", "coordinator")
    workflow.add_edge("output", END)

    # Set the entry point
    workflow.set_entry_point("coordinator")

    # Compile the graph
    return workflow.compile()
{
  "reasoning": "This is a simple factual question asking for the capital of France. The answer is well-known and doesn't require in-depth research, critical analysis, or specialized writing.",
  "next": "done"
}
