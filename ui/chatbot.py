import gradio as gr
from agents.orchestrator import AdvisorOrchestrator

orchestrator = AdvisorOrchestrator()

def respond_chat(user_message: str, history: list) -> tuple:
    """
    Handles user question in AI Stock Advisor Chat tab with Gradio 6.0 messages dict format.
    """
    if not user_message or not user_message.strip():
        return "", history

    if history is None:
        history = []

    response_text = orchestrator.process_chat_query(user_message)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": response_text})
    return "", history

def create_chatbot_tab() -> None:
    """Builds the AI Stock Advisor Chat tab layout in Gradio."""
    gr.Markdown("## 🤖 AI Stock Advisor Chat")
    gr.Markdown(
        "Ask natural-language questions about stocks, companies, industries, or trends. "
        "Requests are routed to specialized sub-agents for financial analysis and plain-language explanation."
    )

    chatbot = gr.Chatbot(
        height=520,
        avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=StockAdvisor")
    )

    with gr.Row():
        msg_input = gr.Textbox(
            placeholder="Type your question here (e.g., 'Analyze NVDA', 'Compare Apple and Microsoft', 'Why is the Software and Cloud industry losing so much?')...",
            show_label=False,
            scale=8
        )
        submit_btn = gr.Button("Send 🚀", variant="primary", scale=1)
        clear_btn = gr.Button("Clear Chat 🗑️", variant="secondary", scale=1)

    gr.Markdown("### 💡 Example Questions")
    examples = [
        "Analyze AAPL for me.",
        "Compare NVIDIA (NVDA) and AMD over the last 6 months.",
        "Why is the software and cloud industry losing so much?",
        "Which industries are performing best right now?",
        "What are the biggest risks facing Tesla (TSLA)?"
    ]
    with gr.Row():
        for ex in examples:
            btn = gr.Button(ex, size="sm", variant="secondary")
            btn.click(fn=lambda text=ex: text, outputs=msg_input)

    # Event handlers
    msg_input.submit(
        fn=respond_chat,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot]
    )
    submit_btn.click(
        fn=respond_chat,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot]
    )
    clear_btn.click(
        fn=lambda: [],
        inputs=None,
        outputs=chatbot,
        queue=False
    )
