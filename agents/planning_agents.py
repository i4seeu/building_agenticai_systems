"""Planning Agents using CrewAI

This module demonstrates multi-agent planning using CrewAI framework.
A planner-writer agent creates a structured plan and then writes content
based on that plan, demonstrating hierarchical task decomposition.

The agent follows a planning-first approach:
1. Create a bullet-point plan for the content
2. Write the final summary based on the plan
3. Return both the plan and summary in a structured report
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


# ============================================================================
# Configuration
# ============================================================================

def load_config():
    """Load environment variables from .env file."""
    load_dotenv("../.env")
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")


# ============================================================================
# Language Model Setup
# ============================================================================

def initialize_llm():
    """Initialize and return the ChatOpenAI language model."""
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
    print("Language Model initialized")
    return llm


# ============================================================================
# Agent Definition
# ============================================================================

def create_planner_writer_agent(llm):
    """
    Create a planner-writer agent that creates plans and writes content.
    
    Args:
        llm: The language model instance to use.
    
    Returns:
        Agent: A configured CrewAI agent with planner-writer role.
    """
    planner_writer_agent = Agent(
        role="Article Planner and Writer",
        goal="Plan and then write a concise, engaging summary on a specified topic.",
        backstory=(
            "You are an expert technical writer and content strategist. "
            "Your strength lies in creating a clear, actionable plan before writing, "
            "ensuring the final summary is both informative and easy to digest."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    return planner_writer_agent


# ============================================================================
# Task Definition
# ============================================================================

def create_planning_task(agent, topic):
    """
    Create a task for planning and writing a summary.
    
    Args:
        agent: The agent to execute the task.
        topic: The topic for the summary.
    
    Returns:
        Task: A configured CrewAI task for planning and writing.
    """
    task = Task(
        description=(
            f"1. Create a bullet-point plan for a summary on the topic: '{topic}'.\n"
            f"2. Write the summary based on your plan, keeping it around 200 words.\n"
            f"3. Ensure the plan is clear and the summary is well-structured."
        ),
        expected_output=(
            "A final report containing two distinct sections:\n\n"
            "### Plan\n"
            "- A bulleted list outlining the main points of the summary.\n\n"
            "### Summary\n"
            "- A concise and well-structured summary of the topic.\n\n"
            "- Keep the summary around 200 words."
        ),
        agent=agent,
    )
    return task


# ============================================================================
# Crew Setup
# ============================================================================

def create_crew(agents, tasks):
    """
    Create and return a CrewAI Crew instance.
    
    Args:
        agents: List of agents for the crew.
        tasks: List of tasks for the crew to execute.
    
    Returns:
        Crew: A configured CrewAI Crew instance.
    """
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    return crew


# ============================================================================
# Main Execution
# ============================================================================

def run_planning_task(topic):
    """
    Execute the planning and writing task for a given topic.
    
    Args:
        topic: The topic to plan and write about.
    
    Returns:
        str: The result from the crew execution.
    """
    print("\n" + "="*80)
    print("PLANNING AGENTS - CONTENT GENERATION")
    print("="*80)
    print(f"\nTopic: {topic}\n")
    
    # Initialize LLM
    llm = initialize_llm()
    
    # Create agent
    agent = create_planner_writer_agent(llm)
    print("✓ Planner-Writer Agent created")
    
    # Create task
    task = create_planning_task(agent, topic)
    print("✓ Planning Task created")
    
    # Create crew
    crew = create_crew([agent], [task])
    print("✓ Crew assembled\n")
    
    # Execute the task
    print("Executing task...\n")
    result = crew.kickoff()
    
    return result


def main():
    """Main entry point for the planning agents script."""
    try:
        load_config()
        
        # Define the topic for planning and writing
        topic = "The importance of Reinforcement Learning in AI"
        
        # Run the planning task
        result = run_planning_task(topic)
        
        # Display results
        print("\n" + "="*80)
        print("TASK RESULT")
        print("="*80)
        print(result)
        print("="*80 + "\n")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    main()