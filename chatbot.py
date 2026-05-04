"""
AI Chatbot using the OpenAI API.

This module provides a terminal-based conversational AI chatbot
that maintains context across messages and optionally saves the
chat history to a file.
"""

import os
import json
import datetime
import sys

from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Load environment variables from a .env file (if present)
load_dotenv()

# Default model to use – can be overridden via the OPENAI_MODEL env var
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# System prompt that defines the chatbot's persona
SYSTEM_PROMPT = (
    "You are a helpful, friendly, and knowledgeable AI assistant. "
    "Answer questions clearly and concisely. "
    "If you don't know something, say so honestly."
)

# Name displayed in the terminal for the assistant
ASSISTANT_NAME = "Assistant"
USER_NAME = "You"


# ---------------------------------------------------------------------------
# OpenAI client initialisation
# ---------------------------------------------------------------------------

def create_client() -> OpenAI:
    """
    Create and return an OpenAI client.

    Reads the API key from the OPENAI_API_KEY environment variable.
    Exits with a helpful message if the key is not set.

    Returns:
        OpenAI: An authenticated OpenAI client instance.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "\n[Error] OPENAI_API_KEY is not set.\n"
            "  1. Copy .env.example to .env\n"
            "  2. Add your OpenAI API key to the .env file\n"
            "  Or export it directly: export OPENAI_API_KEY='your-key'\n"
        )
        sys.exit(1)

    return OpenAI(api_key=api_key)


# ---------------------------------------------------------------------------
# Chat logic
# ---------------------------------------------------------------------------

def build_initial_history() -> list[dict]:
    """
    Return the initial conversation history with the system prompt.

    Returns:
        list[dict]: A list containing the system message.
    """
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def get_response(client: OpenAI, history: list[dict], model: str = DEFAULT_MODEL) -> str:
    """
    Send the conversation history to the OpenAI API and return the reply.

    Args:
        client (OpenAI): The authenticated OpenAI client.
        history (list[dict]): The full conversation history including the latest user message.
        model (str): The OpenAI model to use.

    Returns:
        str: The assistant's reply text.

    Raises:
        OpenAIError: If the API call fails.
    """
    response = client.chat.completions.create(
        model=model,
        messages=history,
    )
    return response.choices[0].message.content


def add_message(history: list[dict], role: str, content: str) -> None:
    """
    Append a message to the conversation history in-place.

    Args:
        history (list[dict]): The conversation history to update.
        role (str): Either "user" or "assistant".
        content (str): The message text.
    """
    history.append({"role": role, "content": content})


# ---------------------------------------------------------------------------
# Chat history persistence (bonus feature)
# ---------------------------------------------------------------------------

def save_history(history: list[dict], filepath: str) -> None:
    """
    Save the conversation history to a JSON file.

    The system prompt message is excluded so the saved file contains
    only human-readable exchanges.

    Args:
        history (list[dict]): The full conversation history.
        filepath (str): Destination file path (e.g. 'chat_history.json').
    """
    # Exclude the system prompt from the saved file
    messages_to_save = [msg for msg in history if msg["role"] != "system"]

    data = {
        "saved_at": datetime.datetime.now().isoformat(),
        "model": DEFAULT_MODEL,
        "messages": messages_to_save,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[Chat history saved to '{filepath}']\n")


# ---------------------------------------------------------------------------
# Terminal UI helpers
# ---------------------------------------------------------------------------

def print_welcome() -> None:
    """Print a welcome banner when the chatbot starts."""
    print("\n" + "=" * 60)
    print("  🤖  AI Chatbot  –  Powered by OpenAI")
    print("=" * 60)
    print("  Type your message and press Enter to chat.")
    print("  Commands:")
    print("    'quit' or 'exit'  – end the conversation")
    print("    'save'            – save chat history to a file")
    print("    'clear'           – start a new conversation")
    print("=" * 60 + "\n")


def print_message(speaker: str, message: str) -> None:
    """
    Print a formatted chat message to the terminal.

    Args:
        speaker (str): The name of the speaker (e.g. 'You' or 'Assistant').
        message (str): The message content.
    """
    print(f"\n{speaker}: {message}\n")


# ---------------------------------------------------------------------------
# Main conversation loop
# ---------------------------------------------------------------------------

def chat_loop(client: OpenAI) -> None:
    """
    Run the interactive conversation loop in the terminal.

    The loop maintains conversation history so the model has context
    for each new message. The user can type commands to save history,
    clear the conversation, or quit.

    Args:
        client (OpenAI): The authenticated OpenAI client.
    """
    history = build_initial_history()
    model = DEFAULT_MODEL
    print_welcome()

    while True:
        # --- Read user input ---
        try:
            user_input = input(f"{USER_NAME}: ").strip()
        except (KeyboardInterrupt, EOFError):
            # Allow Ctrl+C / Ctrl+D to exit gracefully
            print("\n\n[Goodbye!]\n")
            break

        # --- Handle empty input ---
        if not user_input:
            continue

        # --- Handle special commands ---
        command = user_input.lower()

        if command in ("quit", "exit"):
            print("\n[Goodbye! Have a great day!]\n")
            break

        if command == "save":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"chat_history_{timestamp}.json"
            save_history(history, filepath)
            continue

        if command == "clear":
            history = build_initial_history()
            print("\n[Conversation cleared. Starting fresh!]\n")
            continue

        # --- Add user message to history ---
        add_message(history, "user", user_input)

        # --- Get assistant response ---
        try:
            reply = get_response(client, history, model)
        except OpenAIError as exc:
            # Surface API errors without crashing the loop
            print(f"\n[API Error] {exc}\n")
            # Remove the failed user message so the history stays consistent
            history.pop()
            continue

        # --- Add assistant reply to history and display it ---
        add_message(history, "assistant", reply)
        print_message(ASSISTANT_NAME, reply)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Initialise the client and start the chat loop."""
    client = create_client()
    chat_loop(client)


if __name__ == "__main__":
    main()
