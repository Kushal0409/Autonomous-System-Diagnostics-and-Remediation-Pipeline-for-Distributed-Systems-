import gradio as gr
import os
from dotenv import load_dotenv
from agents import IncidentAgents

# Load environment variables
load_dotenv()

# ---  DEFAULT DATA 
DEFAULT_LOGS = """"""

DEFAULT_TICKET = """"""

DEFAULT_RUNBOOK = """"""

# --- 2. THE CORE WORKFLOW FUNCTION ---
def run_incident_response(logs_input, ticket_input, runbook_input):
    """
    This function connects the UI inputs to the Agent Logic.
    """
    try:
        # Initialize Agents
        agents = IncidentAgents()
        
        # Step A: Log Analysis
        log_analysis = agents.log_analysis_agent(logs_input)
        yield log_analysis, "...", "...", "...", "..." # Stream updates to UI

        # Step B: Correlation
        correlation = agents.incident_correlator_agent(ticket_input, log_analysis)
        yield log_analysis, correlation, "...", "...", "..."

        # Step C: Root Cause Analysis
        rca = agents.root_cause_agent(correlation, runbook_input)
        yield log_analysis, correlation, rca, "...", "..."

        # Step D: Resolution
        resolution = agents.resolution_agent(rca, runbook_input)
        yield log_analysis, correlation, rca, resolution, "..."

        # Step E: Final Report
        final_report = agents.report_agent(ticket_input, rca, resolution)
        yield log_analysis, correlation, rca, resolution, final_report

    except Exception as e:
        error_msg = f" Error: {str(e)}"
        yield error_msg, error_msg, error_msg, error_msg, error_msg

# --- 3. BUILD THE GRADIO UI ---
with gr.Blocks(title="Agentic Incident Response", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.Markdown("#  AI Agent Incident Response System")
    gr.Markdown("Enter system logs, an incident ticket, and a runbook. The Multi-Agent System will analyze, correlate, and fix the issue.")

    # Input Section
    with gr.Row():
        with gr.Column():
            logs_box = gr.Textbox(label="1. System Logs", value=DEFAULT_LOGS, lines=8, placeholder="Paste logs here...")
        with gr.Column():
            ticket_box = gr.Textbox(label="2. Incident Ticket (JSON)", value=DEFAULT_TICKET, lines=8, placeholder="Paste ticket JSON here...")
        with gr.Column():
            runbook_box = gr.Textbox(label="3. Runbook (Markdown)", value=DEFAULT_RUNBOOK, lines=8, placeholder="Paste runbook here...")

    # Action Button
    run_btn = gr.Button(" Run Automated Response Workflow", variant="primary")

    # Output Section (The "Agent Minds")
    gr.Markdown("###  Agent Reasoning Chain")
    
    with gr.Accordion("Step 1: Log Analysis Agent", open=False):
        out_logs = gr.Markdown()
    
    with gr.Accordion("Step 2: Incident Correlator Agent", open=False):
        out_correlation = gr.Markdown()
    
    with gr.Accordion("Step 3: Root Cause Analysis (RCA) Agent", open=False):
        out_rca = gr.Markdown()

    with gr.Accordion("Step 4: Resolution Agent", open=True):
        out_resolution = gr.Markdown()

    # Final Report Section
    gr.Markdown("###  Final Post-Incident Report")
    out_final_report = gr.Markdown()

    # Click Event
    run_btn.click(
        fn=run_incident_response,
        inputs=[logs_box, ticket_box, runbook_box],
        outputs=[out_logs, out_correlation, out_rca, out_resolution, out_final_report]
    )

# Launch
if __name__ == "__main__":
    demo.launch()