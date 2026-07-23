import gradio as gr
import logging
import sys

from ui.dashboard import create_dashboard_tab
from ui.chatbot import create_chatbot_tab

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def build_app() -> gr.Blocks:
    """Builds the main Gradio application with center-aligned layout and consistent chart styling."""
    custom_css = """
    .gradio-container {
        max-width: 1500px !important;
        margin: 0 auto !important;
        padding-left: 24px !important;
        padding-right: 24px !important;
    }
    .tabs {
        display: flex !important;
        justify-content: center !important;
    }
    .tab-nav {
        display: flex !important;
        justify-content: center !important;
        gap: 16px !important;
        border-bottom: 2px solid #334155 !important;
        margin-bottom: 24px !important;
    }
    .tab-nav button {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
    }
    .js-plotly-plot, .plot-container {
        min-height: 600px !important;
        height: 600px !important;
    }
    """

    with gr.Blocks(css=custom_css) as demo:
        gr.HTML(
            """
            <div style="text-align: center; padding: 24px 0; background: linear-gradient(90deg, #1E1B4B 0%, #312E81 50%, #1E1B4B 100%); color: white; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
                <h1 style="margin: 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -0.02em;">📊 Stock Market Analysis Agent</h1>
                <p style="margin: 6px 0 0 0; color: #A5B4FC; font-size: 1.05rem;">Multi-Agent AI Market Analytics & Layman Financial Explanation</p>
            </div>
            """
        )

        with gr.Tabs() as tabs:
            with gr.TabItem("📈 Market Dashboard", id="dashboard_tab"):
                initial_load_fn, dashboard_outputs = create_dashboard_tab()

            with gr.TabItem("🤖 AI Stock Advisor", id="chatbot_tab"):
                create_chatbot_tab()

        demo.load(fn=initial_load_fn, outputs=dashboard_outputs)

    return demo

app = build_app()

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
