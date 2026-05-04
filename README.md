# 🤖 AI Chatbot

A clean, modular terminal-based AI chatbot built with Python and the **OpenAI API**. Designed as a portfolio-quality project for junior developers targeting remote AI/ML roles.

---

## ✨ Features

| Feature | Detail |
|---|---|
| 💬 Continuous conversation | The chatbot remembers the full conversation context across turns |
| 🔑 Secure API key handling | API key loaded from an environment variable – never hard-coded |
| 🛡️ Robust error handling | Graceful recovery from API errors, empty input, and keyboard interrupts |
| 💾 Save chat history | Type `save` at any time to export the conversation to a timestamped JSON file |
| 🔄 Clear conversation | Type `clear` to reset the chat without restarting the program |
| 🧩 Modular design | Clean separation of concerns: client setup, chat logic, persistence, and UI |

---

## 🛠️ Technologies

- **Python 3.10+**
- **[OpenAI Python SDK](https://github.com/openai/openai-python)** (`openai >= 1.30`)
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** – loads `.env` files for environment variable management
- Model: `gpt-4o-mini` (configurable via the `OPENAI_MODEL` env var)

---

## 📁 Project Structure

```
ai-chatbot/
├── chatbot.py          # Main chatbot application
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore          # Excludes secrets and cache files
└── README.md           # This file
```

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/jjpalacioz/ai-chatbot.git
cd ai-chatbot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example env file and add your [OpenAI API key](https://platform.openai.com/api-keys):

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder value:

```env
OPENAI_API_KEY=sk-...your-real-key-here...
```

> **Security tip:** `.env` is listed in `.gitignore` and will **never** be committed to the repository.

### 5. Run the chatbot

```bash
python chatbot.py
```

---

## 💡 Usage

Once running, type any message and press **Enter**. The assistant replies immediately and remembers the full conversation.

### Available commands

| Command | Action |
|---|---|
| `quit` or `exit` | End the session |
| `save` | Save the chat history to `chat_history_<timestamp>.json` |
| `clear` | Wipe the conversation and start fresh |
| `Ctrl+C` | Exit gracefully at any time |

---

## 🗨️ Example Conversation

```
============================================================
  🤖  AI Chatbot  –  Powered by OpenAI
============================================================
  Type your message and press Enter to chat.
  Commands:
    'quit' or 'exit'  – end the conversation
    'save'            – save chat history to a file
    'clear'           – start a new conversation
============================================================

You: Hi! Can you explain what machine learning is in simple terms?
Assistant: Sure! Machine learning is a way of teaching computers to learn from
examples rather than giving them explicit rules. Think of it like training a dog:
instead of telling the dog every single rule, you reward it when it does the right
thing until it figures out the pattern on its own.

In technical terms, a model looks at lots of data, finds patterns, and uses those
patterns to make predictions on new, unseen data.

You: What are some real-world examples?

Assistant: Great question! Here are a few everyday examples:

- **Email spam filters** - learn which emails are spam from past examples.
- **Recommendation engines** - Netflix and Spotify suggest content based on your history.
- **Voice assistants** - Siri and Alexa understand speech using ML models.
- **Fraud detection** - banks flag unusual transactions in real time.

You: Awesome, thank you!

Assistant: You're welcome! Feel free to ask anything else.

You: save

[Chat history saved to 'chat_history_20240601_143022.json']

You: exit

[Goodbye! Have a great day!]
```

---

## Saved Chat History (JSON)

When you type `save`, the conversation is exported as a structured JSON file:

```json
{
  "saved_at": "2024-06-01T14:30:22.123456",
  "model": "gpt-4o-mini",
  "messages": [
    { "role": "user", "content": "Hi! Can you explain what machine learning is?" },
    { "role": "assistant", "content": "Sure! Machine learning is a way of..." }
  ]
}
```

---

## Ideas for Future Improvements

- Add a web interface with Flask or FastAPI
- Support multiple AI providers (Anthropic Claude, Google Gemini)
- Add streaming responses for a real-time typing effect
- Implement a conversation summary to manage very long chats
- Add a configurable system prompt at startup

---

## Author

Built as a portfolio project demonstrating real-world Python, OpenAI API integration,
and software engineering best practices.

---

## License

MIT - free to use and modify.
