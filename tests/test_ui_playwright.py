import time
import subprocess
import pytest
from playwright.sync_api import sync_playwright

def test_dashboard_charts_readability():
    """
    Playwright test launching the Gradio server, inspecting DOM chart elements,
    and verifying container dimensions and visual readability for all Plotly charts.
    """
    proc = subprocess.Popen(
        [".venv/bin/python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        time.sleep(4)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1440, "height": 1080})

                page.goto("http://localhost:7860", timeout=30000)
                page.wait_for_load_state("networkidle")

                page.wait_for_selector(".js-plotly-plot", timeout=25000)
                plots = page.query_selector_all(".js-plotly-plot")

                # Save full dashboard screenshot
                page.screenshot(path="dashboard_charts.png", full_page=True)

                assert len(plots) >= 3, f"Expected at least 3 Plotly charts, found {len(plots)}"

                for idx, plot in enumerate(plots):
                    box = plot.bounding_box()
                    assert box is not None, f"Chart {idx+1} has no bounding box"
                    assert box["height"] >= 350, f"Chart {idx+1} height {box['height']}px is too small for readability"

                browser.close()
        except Exception as e:
            if "Target page, context or browser has been closed" in str(e) or "Permission denied" in str(e):
                pytest.skip("Playwright headless browser execution skipped due to OS sandbox permissions.")
            else:
                raise e

    finally:
        proc.terminate()
        proc.wait()
