"""
Gradio Interface for AI Agent
"""

import gradio as gr
from agent import AIAgent

print("🤖 Initializing AI Agent...")
agent = AIAgent()
print("✅ Agent ready!")

def respond(message, chat_history):
    if not message:
        return "", chat_history
    
    result = agent.ask(message)
    chat_history.append((message, result['answer']))
    return "", chat_history

with gr.Blocks(title="AI Agent") as demo:
    gr.Markdown("""
    # 🤖 AI Agent with Tool Calling
    
    I can use tools to help answer your questions!
    
    **Available Tools:**
    - 🧮 Calculator
    - ⏰ Current Time
    - 🌤️ Weather
    - 📝 Word Counter
    - 📚 Wikipedia
    """)
    
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(placeholder="Type your question here...")
    
    with gr.Row():
        send_btn = gr.Button("Send", variant="primary")
        clear_btn = gr.Button("Clear")
    
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: ([], ""), outputs=[chatbot, msg])

if __name__ == "__main__":
    demo.launch(share=True)
