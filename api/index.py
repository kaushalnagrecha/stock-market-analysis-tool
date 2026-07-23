import os
import sys

# Ensure root project directory is on sys.path for Vercel serverless execution
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import gradio as gr

from data.providers.industry_provider import IndustryProvider
from app import build_app

# Initialize FastAPI application
app = FastAPI(
    title="Stock Advisor Agent",
    description="Multi-Agent AI Market Analytics API & Gradio UI for Vercel",
    version="1.0.0"
)

@app.get("/api/health")
def health_check():
    """Health check endpoint for Vercel monitoring."""
    return {"status": "ok", "platform": "Vercel Serverless"}

@app.get("/api/industries")
def get_all_industries():
    """
    API Endpoint returning the broadened market industry spectrum,
    constituent companies, and industry metrics.
    """
    return IndustryProvider.get_api_payload()

@app.get("/api/universe")
def get_symbol_universe():
    """
    API Endpoint returning the complete Ticker -> Company & Industry mapping.
    """
    return {
        "status": "success",
        "total_symbols": len(IndustryProvider.get_symbol_map()),
        "symbols": IndustryProvider.get_symbol_map()
    }

# Build Gradio Blocks demo
gradio_demo = build_app()

# Mount Gradio Blocks application onto FastAPI root
app = gr.mount_gradio_app(app, gradio_demo, path="/")
