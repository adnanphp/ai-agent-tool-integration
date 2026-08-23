"""
AI Agent Using Ollama's Native Tool Calling
Works with models that support tools (llama3.2, phi, etc.)
"""

import json
import requests
from datetime import datetime
import math

OLLAMA_URL = "http://localhost:11434/api/chat"

def ask_ollama_with_tools(model, question):
    """Send a question to Ollama with tool definitions"""
    
    # Define tools in Ollama's format
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Performs basic math operations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The math expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Returns the current date and time"
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Gets weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city name"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]
    
    # Function implementations
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
        return weather_data.get(city.lower(), f"🌤️ Weather for {city} not available")
    
    # Available functions
    functions = {
        "calculator": calculator,
        "get_current_time": get_current_time,
        "get_weather": get_weather
    }
    
    # Prepare the request
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "tools": tools,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        result = response.json()
        
        # Check if the model wants to call a tool
        message = result.get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        if tool_calls:
            # Execute the tool
            tool_call = tool_calls[0]
            tool_name = tool_call["function"]["name"]
            tool_args = json.loads(tool_call["function"]["arguments"])
            
            # Call the function
            if tool_name in functions:
                result_str = functions[tool_name](**tool_args)
                return f"Tool result: {result_str}"
            else:
                return f"Unknown tool: {tool_name}"
        
        # If no tool call, return the model's response
        return message.get("content", "No response")
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 AI Agent with Ollama Tool Calling")
    print("=" * 50)
    print("Make sure Ollama is running and llama3.2:3b is pulled:")
    print("  ollama pull llama3.2:3b")
    print()
    
    # Try with llama3.2 (supports tools)
    model = "llama3.2:3b"
    
    questions = [
        "What is 25 * 18?",
        "What time is it?",
        "What is the weather in Paris?"
    ]
    
    for q in questions:
        print("-" * 40)
        print(f"❓ {q}")
        result = ask_ollama_with_tools(model, q)
        print(f"🤖 {result}")
        print("-" * 40)
    
    print("\n🎉 Test complete!")
