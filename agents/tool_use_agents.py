import os, getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_agent
# --- Configuration ---
# Load environment variables from .env file (for OPENAI_API_KEY)
load_dotenv("../.env")
# Check if the API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file. Pleaseadd it.")
try:
    # A model with function/tool calling capabilities is required.
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("Language model initialized")
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None

# --- Define Tools ---
# --- Define a Tool ---
@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool to
    find answers to phrases
    like 'capital of France' or 'weather in London?'.
    """
    print(f"\n--- 🛠 Tool Called: search_information with query:'{query}' ---")
    # Simulate a search tool with a dictionary of predefined results.
    simulated_results = {
    "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
    "capital of france": "The capital of France is Paris.",
    "population of earth": "The estimated population of Earth is around 8 billion people.",
    "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
    "default": f"Simulated search result for '{query}': No specific information found, but the topic seems interesting."
    }
    result = simulated_results.get(query.lower(),
    simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result
tools = [search_information]

# --- Create the Agent ---
# The new create_agent API uses 'model' (not 'llm') and returns a compiled StateGraph
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant that uses tools to answer user questions accurately.",
    debug=True,
)

# --- Run the Agent ---
def run_tool_use_agent():
    """
    Demonstrates an agent that uses tools to answer user queries.
    Uses the new LangGraph streaming API.
    """
    print("\n=== Tool-Using Agent Demo ===")
    user_queries = [
        "What is the capital of France?",
        "Can you tell me the weather in London?",
        "What's the population of Earth?",
        "Which is the tallest mountain?",
        "Tell me something interesting about quantum computing."
    ]
    for query in user_queries:
        print(f"\n>>> User Query: {query}")
        try:
            # Use the new LangGraph streaming API
            for event in agent.stream(
                {"messages": [{"role": "user", "content": query}]},
                stream_mode="updates"
            ):
                # Process each event from the stream
                if "agent" in event:
                    agent_output = event["agent"]
                    if "messages" in agent_output:
                        for msg in agent_output["messages"]:
                            if hasattr(msg, "content"):
                                print(f"\n--- Agent Response ---\n{msg.content}\n")
        except Exception as e:
            print(f"Error processing query: {e}")

if __name__ == "__main__":
    run_tool_use_agent()