"""
AI Agent with TinyLlama - Improved Tool Prompt
Forces the model to actually use tools
"""

import requests
import json
import re
from datetime import datetime
import math

OLLAMA_URL = "http://localhost:11434/api/generate"

# Define our "tools" as Python functions
def calculator(expression):
    try:
        allowed = set('0123456789+-*/(). ')
        if any(c not in allowed for c in expression):
            return "Error: Invalid expression"
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city):
    weather_data = {
        "london": "🌧️ 15°C, Rainy",
        "paris": "☀️ 22°C, Sunny",
        "new york": "⛅ 18°C, Partly Cloudy",
        "tokyo": "🌧️ 20°C, Rainy",
        "sydney": "☀️ 28°C, Sunny"
    }
    return weather_data.get(city.lower(), f"🌤️ Unknown weather for {city}")

# Map tool names to functions
TOOL_FUNCTIONS = {
    "CALCULATE": calculator,
    "TIME": get_current_time,
    "WEATHER": get_weather
}

def ask_tinyllama_with_tools(question):
    """Ask TinyLlama to use tools with strict formatting"""
    
    # Simplified prompt with examples
    prompt = f"""You are a tool-using AI. When asked a question, you MUST respond with ONLY one of these formats:

For math: [CALCULATE: 25*18]
For time: [TIME]
For weather: [WEATHER: Paris]

If you don't know, respond with: [UNKNOWN]

Question: {question}

Your response (ONLY the format, nothing else):"""
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1,  # Lower temperature for more consistent output
                "max_tokens": 50
            },
            timeout=60
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        
        result = response.json().get("response", "").strip()
        
        # Try to parse the response
        # Check for tool patterns
        if "[CALCULATE:" in result:
            match = re.search(r"\[CALCULATE:\s*([^\]]+)\]", result)
            if match:
                expr = match.group(1).strip()
                return f"🧮 {calculator(expr)}"
        
        if "[TIME]" in result:
            return f"⏰ {get_current_time()}"
        
        if "[WEATHER:" in result:
            match = re.search(r"\[WEATHER:\s*([^\]]+)\]", result)
            if match:
                city = match.group(1).strip()
                return f"🌤️ {get_weather(city)}"
        
        if "[UNKNOWN]" in result:
            return "❓ I don't know how to answer that."
        
        # If no tool pattern, try to extract the answer directly
        if result:
            return f"💬 {result[:200]}"
        
        return "❓ No response"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TinyLlama with Improved Tool Prompts")
    print("=" * 50)
    print()
    
    questions = [
        "What is 25 * 18?",
        "What time is it?",
        "What is the weather in Paris?"
    ]
    
    for q in questions:
        print("-" * 40)
        print(f"❓ {q}")
        result = ask_tinyllama_with_tools(q)
        print(f"🤖 {result}")
        print("-" * 40)
    
    print("\n🎉 Test complete!")
