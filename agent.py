"""
AI Agent with LangGraph 1.x - Using langchain-ollama
No deprecated imports!
"""

from typing import Dict, List, Any
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama  # New import!
from langchain_core.messages import HumanMessage
from datetime import datetime
import math

# ========== Define Tools ==========

@tool
def calculator(expression: str) -> str:
    """Performs basic math operations."""
    try:
        allowed = set('0123456789+-*/(). ')
        if any(c not in allowed for c in expression):
            return "Error: Only basic math operations allowed"
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_current_time() -> str:
    """Returns the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def get_weather(city: str) -> str:
    """Gets mock weather for a city."""
    weather_data = {
        "london": "🌧️ 15°C, Rainy",
        "paris": "☀️ 22°C, Sunny",
        "new york": "⛅ 18°C, Partly Cloudy",
        "tokyo": "🌧️ 20°C, Rainy",
        "sydney": "☀️ 28°C, Sunny"
    }
    city_lower = city.lower().strip()
    for key in weather_data:
        if key in city_lower:
            return weather_data[key]
    return f"🌤️ Weather not available for '{city}'. Try: London, Paris, New York, Tokyo, Sydney"

@tool
def word_counter(text: str) -> str:
    """Counts words in the provided text."""
    words = text.split()
    return f"Word count: {len(words)}"

@tool
def wikipedia_search(query: str) -> str:
    """Searches Wikipedia for information."""
    try:
        import wikipedia
        summary = wikipedia.summary(query, sentences=2)
        return f"Wikipedia: {summary}"
    except ImportError:
        return "Error: wikipedia not installed. Run: pip install wikipedia"
    except Exception as e:
        return f"Error: {str(e)}"

# ========== Create Agent ==========

def create_agent():
    """Initialize the LangGraph agent with tools"""
    
    tools = [
        calculator,
        get_current_time,
        get_weather,
        word_counter,
        wikipedia_search
    ]
    
    # Use the new ChatOllama from langchain-ollama
    try:
        llm = ChatOllama(model="tinyllama", base_url="http://localhost:11434")
        # Test connection
        llm.invoke("Hello")
        print("✅ Connected to Ollama with tinyllama")
    except Exception as e:
        print(f"⚠️ Ollama connection error: {e}")
        print("Make sure Ollama is running and model is pulled:")
        print("  ollama serve")
        print("  ollama pull tinyllama")
        return None
    
    # Create agent using LangGraph's create_react_agent
    agent = create_react_agent(
        model=llm,
        tools=tools
    )
    
    return agent

# ========== AIAgent Class ==========

class AIAgent:
    def __init__(self):
        self.agent = create_agent()
        if self.agent is None:
            print("⚠️ Agent initialization failed.")
    
    def ask(self, question: str) -> Dict:
        """Ask the agent a question"""
        if self.agent is None:
            return {"question": question, "answer": "Error: Agent not initialized."}
        
        try:
            print(f"🤔 Thinking about: {question}")
            result = self.agent.invoke({"messages": [HumanMessage(content=question)]})
            final_message = result["messages"][-1]
            answer = final_message.content if hasattr(final_message, 'content') else str(final_message)
            return {"question": question, "answer": answer}
        except Exception as e:
            return {"question": question, "answer": f"Error: {str(e)}"}

# ========== Test ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Agent with Tool Calling (LangGraph + langchain-ollama)")
    print("=" * 50)
    print("Make sure Ollama is running and tinyllama is pulled:")
    print("  ollama serve")
    print("  ollama pull tinyllama")
    print()
    
    agent = AIAgent()
    if agent.agent is None:
        exit(1)
    
    test_questions = [
        "What is 25 * 18?",
        "What time is it?",
        "What is the weather in Paris?",
        "Count the words in: Hello world, this is a test."
    ]
    
    for q in test_questions:
        print("\n" + "-" * 40)
        print(f"❓ {q}")
        result = agent.ask(q)
        print(f"🤖 {result['answer']}")
        print("-" * 40)
    
    print("\n🎉 Agent test complete!")
