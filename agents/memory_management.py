"""
Simple example of LangChain message history management.

This module demonstrates how to use a simple in-memory message history
to store and manage conversation messages between a user and an AI.
"""

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class SimpleMemoryHistory:
    """A simple in-memory message history manager."""

    def __init__(self):
        """Initialize an empty message list."""
        self.messages: list[BaseMessage] = []

    def add_user_message(self, content: str) -> None:
        """Add a user message to history."""
        self.messages.append(HumanMessage(content=content))

    def add_ai_message(self, content: str) -> None:
        """Add an AI message to history."""
        self.messages.append(AIMessage(content=content))

    def get_messages(self):
        """Return all messages."""
        return self.messages


def main() -> None:
    """Initialize and manage a simple conversation history."""
    # Initialize the history object
    history = SimpleMemoryHistory()

    # Add user and AI messages
    history.add_user_message("I'm heading to New York next week.")
    history.add_ai_message("Great! It's a fantastic city.")

    # Access the list of messages
    print("Conversation History:")
    for msg in history.get_messages():
        print(f"  {msg.type}: {msg.content}")


if __name__ == "__main__":
    main()