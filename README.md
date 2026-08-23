# 🤖 AI Agent with Tool Integration

[![GitHub](https://img.shields.io/badge/GitHub-Repo-blue)](https://github.com/adnanphp/ai-agent)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-TinyLlama-green)](https://ollama.com)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange)](https://gradio.app)

## 📋 Overview

An intelligent AI agent that integrates with external tools to answer questions and perform tasks. Built with **TinyLlama**, **LangGraph**, and **Gradio**.

### 🎯 Features

- 🧮 **Calculator Tool** - Perform mathematical operations
- ⏰ **Time Tool** - Get current date and time
- 🌤️ **Weather Tool** - Get weather for major cities
- 💬 **Natural Language Understanding** - Ask questions in plain English
- 🌐 **Web Interface** - Interactive Gradio UI
- 🔌 **Extensible Architecture** - Easy to add new tools

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **TinyLlama** | Local LLM (637 MB) |
| **LangChain** | Agent framework |
| **Gradio** | Web interface |
| **Python** | Backend |
| **Ollama** | LLM server |

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/adnanphp/ai-agent.git
cd ai-agent

# Install dependencies
pip install -r requirements.txt

# Make sure Ollama is running
ollama serve

# Pull the model (if not already)
ollama pull tinyllama

# Run the agent
python agent_simple.py
📁 Project Structure
text
ai-agent/
├── agent_simple.py           # Direct TinyLlama agent
├── agent_tool_prompt.py      # Tool prompt version
├── agent_tool_prompt_v2.py   # Improved tool version
├── agent_tool_prompt_final.py # Final working version
├── app.py                    # Gradio web interface
├── requirements.txt          # Dependencies
└── README.md                 # Documentation
🔧 Available Tools
Tool	Description	Example
Calculator	Performs math operations	"What is 25 * 18?"
Time	Returns current date/time	"What time is it?"
Weather	Gets weather for a city	"What is the weather in Paris?"
📊 Example Usage
python
from agent_simple import ask_tinyllama

# Ask a question
response = ask_tinyllama("What is 25 * 18?")
print(response)
# Output: 25 * 18 = 450
📸 Screenshot
(Add a screenshot of the Gradio interface here)

📝 License
MIT

👨‍💻 Author
Adnan - GitHub

🔗 Live Demo: (Add Hugging Face Space URL when deployed)
