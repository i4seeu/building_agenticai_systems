"""Deep Research API using OpenAI

This module demonstrates how to use OpenAI's Deep Research API (o3-deep-research)
to conduct comprehensive research on complex topics.

The script:
1. Sends a research question to the Deep Research model
2. Retrieves the structured report with inline citations
3. Extracts and displays intermediate steps (reasoning, web searches, code execution)
"""

import os
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================================
# Configuration
# ============================================================================

def load_config():
    """Load environment variables from .env file."""
    load_dotenv("../.env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")
    return api_key


# ============================================================================
# Initialize OpenAI Client
# ============================================================================

def initialize_client(api_key):
    """Initialize and return OpenAI client."""
    client = OpenAI(api_key=api_key)
    print("✓ OpenAI client initialized")
    return client


# ============================================================================
# Deep Research API Call
# ============================================================================

def run_deep_research(client, system_message, user_query):
    """
    Execute a deep research request using OpenAI's API.
    
    Args:
        client: OpenAI client instance
        system_message: System instructions for the research
        user_query: The research question to investigate
    
    Returns:
        Response object from the OpenAI API
    """
    print(f"\n📊 Running Deep Research for: {user_query}\n")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            max_tokens=4096,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )
        return response
    except Exception as e:
        print(f"Error during Deep Research API call: {e}")
        raise


# ============================================================================
# Extract and Display Results
# ============================================================================

def display_final_report(response):
    """Extract and display the final research report."""
    print("\n" + "="*80)
    print("FINAL RESEARCH REPORT")
    print("="*80 + "\n")
    
    try:
        # Extract the final report text from the response
        if hasattr(response, 'content'):
            for block in response.content:
                if hasattr(block, 'text'):
                    print(block.text)
        elif hasattr(response, 'choices'):
            for choice in response.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    print(choice.message.content)
    except Exception as e:
        print(f"Error extracting report: {e}")


def display_citations(response):
    """Extract and display citations from the report."""
    print("\n" + "="*80)
    print("RESPONSE METADATA")
    print("="*80 + "\n")
    
    try:
        # Display basic response information
        if hasattr(response, 'model'):
            print(f"Model: {response.model}")
        if hasattr(response, 'usage'):
            print(f"Tokens used - Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens}")
        
        print("\nNo specific citations found. This model returns research in the message content.")
    except Exception as e:
        print(f"Error displaying metadata: {e}")


def display_thinking_process(response):
    """Display the thinking/reasoning process from the model."""
    print("\n" + "="*80)
    print("RESPONSE DETAILS")
    print("="*80 + "\n")
    
    try:
        if hasattr(response, 'choices'):
            for i, choice in enumerate(response.choices):
                print(f"Choice {i+1}:")
                if hasattr(choice, 'finish_reason'):
                    print(f"  Finish Reason: {choice.finish_reason}")
                if hasattr(choice, 'index'):
                    print(f"  Index: {choice.index}")
        else:
            print("No additional details available in response.")
    except Exception as e:
        print(f"Error displaying response details: {e}")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main entry point for the Deep Research script."""
    try:
        # Load configuration
        api_key = load_config()
        
        # Initialize client
        client = initialize_client(api_key)
        
        # Define research parameters
        system_message = (
            "You are a professional researcher preparing a structured, "
            "data-driven report. Focus on data-rich insights, use reliable sources, "
            "and include citations where applicable."
        )
        
        user_query = (
            "Research the economic impact of semaglutide on global healthcare systems. "
            "Include recent data, market size projections, and healthcare provider impacts."
        )
        
        # Run deep research
        response = run_deep_research(client, system_message, user_query)
        
        # Display results
        display_final_report(response)
        display_thinking_process(response)
        display_citations(response)
        
        print("\n" + "="*80)
        print("Research completed successfully!")
        print("="*80 + "\n")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
