"""
AI Agent with TinyLlama - Using Prompt Engineering for Tools
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
    }
    return weather_data.get(city.lower(), f"🌤️ Unknown weather for {city}")

def ask_tinyllama_with_tools(question):
    """Ask TinyLlama to decide which tool to use"""
    
    # Prompt with tool descriptions
    prompt = f"""You have access to these tools:
- CALCULATE: for math (e.g., "CALCULATE: 25*18")
- TIME: for current time
- WEATHER: for weather (e.g., "WEATHER: Paris")

Question: {question}

If you need a tool, respond with only the tool command.
If you can answer directly, just give the answer.

Response:"""
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,
                "max_tokens": 100
            },
            timeout=60
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        
        result = response.json().get("response", "").strip()
        
        # Parse the response
        if result.startswith("CALCULATE:"):
            expr = result.replace("CALCULATE:", "").strip()
            return f"🧮 {calculator(expr)}"
        elif result.startswith("TIME"):
            return f"⏰ {get_current_time()}"
        elif result.startswith("WEATHER:"):
            city = result.replace("WEATHER:", "").strip()
            return f"🌤️ {get_weather(city)}"
        else:
            return f"💬 {result}"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 TinyLlama with Tool Prompts")
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
