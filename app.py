"""
Gradio Web Interface for AI Agent - Gradio 6.x Compatible (Fixed)
"""

import gradio as gr
import re
from datetime import datetime
import math

# ========== Tool Functions ==========

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
        "sydney": "☀️ 28°C, Sunny",
        "toronto": "❄️ -2°C, Snowy"
    }
    return weather_data.get(city.lower(), f"🌤️ Weather for '{city}' not available")

# ========== Agent Function ==========

def ask_agent(question):
    if not question or not question.strip():
        return "Please ask a question."
    
    question_lower = question.lower()
    
    # Weather
    if any(word in question_lower for word in ["weather", "temperature", "rain", "sunny"]):
        city_match = re.search(r"in\s+([A-Za-z\s]+)", question)
        if city_match:
            city = city_match.group(1).strip()
        else:
            words = question.split()
            for word in words:
                if word[0].isupper() and len(word) > 2:
                    city = word
                    break
            else:
                return "🌤️ Please specify a city (e.g., 'What is the weather in Paris?')"
        return f"🌤️ {get_weather(city)}"
    
    # Time
    if any(word in question_lower for word in ["time", "date", "today", "clock"]):
        return f"⏰ {get_current_time()}"
    
    # Calculator
    if any(word in question_lower for word in ["calculate", "*", "+", "-", "/"]):
        math_match = re.search(r"[\d.]+\s*[+\-*/]\s*[\d.]+", question)
        if math_match:
            return f"🧮 {calculator(math_match.group())}"
    
    return "💬 I can help with:\n- Math (e.g., 'What is 15 * 7?')\n- Time (e.g., 'What time is it?')\n- Weather (e.g., 'What is the weather in Paris?')"

# ========== Gradio Interface (Working Version) ==========

# The correct format for Gradio 6.x ChatInterface
def chat_function(message, history):
    """
    This is the function that ChatInterface expects.
    It must return a string response.
    """
    if not message:
        return "Please ask a question."
    
    response = ask_agent(message)
    return response

# Create the interface
demo = gr.ChatInterface(
    fn=chat_function,
    title="🤖 AI Agent with Tool Integration",
    description=("Ask me anything! I can do math, tell time, and check weather."),
    examples=[
        "What is 25 * 18?",
        "What time is it?",
        "What is the weather in Paris?",
        "What is 15 + 7?",
        "What's the weather in London?"
    ]
)

if __name__ == "__main__":
    demo.launch(share=True)
