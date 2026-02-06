# Automated Incident Response System

Built an agentic AI system designed to simulate the workflow of a Site Reliability Engineer (SRE). It autonomously ingests raw server logs, correlates them with incident tickets, and consults engineering runbooks to identify root causes and propose remediation steps.

Unlike standard chatbots, this project implements a **Multi-Agent Architecture** where distinct AI personas (Log Analyst, Incident Commander, Root Cause Expert) collaborate sequentially to solve a problem. This separation of concerns improves accuracy and reduces hallucinations by grounding each step in specific data sources.

## Key Features

- **Autonomous Log Analysis**: Parses unstructured server logs to extract error patterns, timestamps, and failure signals without complex Regex rules.
- **Incident Correlation**: Cross-references technical log data with user-reported symptoms in JSON tickets to verify incidents.
- **Runbook-Grounded Resolution**: Uses a "Retrieval-Augmented" approach to fetch specific remediation commands from Markdown documentation, ensuring proposed fixes are valid.
- **Structured Reporting**: Automatically generates professional Post-Incident Reports (PIRs), including executive summaries and timeline reconstruction.
- **Transparent Logic**: Includes a Gradio interface to visualize the step-by-step reasoning chain of the agents.

## System Architecture

The system is built on a sequential workflow:

1.  **Log Analysis Agent**: Ingests raw text logs and outputs a technical summary of anomalies.
2.  **Correlation Agent**: Compares the technical summary with the incident ticket to confirm the scope of the issue.
3.  **Root Cause Agent**: Analyzes the confirmed symptoms against the Engineering Runbook to identify the underlying cause.
4.  **Resolution Agent**: Extracts the specific mitigation steps associated with that root cause.
5.  **Report Agent**: Synthesizes all prior outputs into a final Markdown report.

## Technology Stack

- **Core Logic**: Python
- **Inference Engine**: Google Gemini API (via `google-generativeai`)
- **Interface**: Gradio (for web-based demonstration)
- **Environment Management**: Python Dotenv

## Installation and Setup

**1. Clone the repository**
git clone [https://github.com/Kushal0409/Autonomous-System-Diagnostics.git](https://github.com/Kushal0409/Autonomous-System-Diagnostics.git)
cd Autonomous-System-Diagnostics

**2 Install the dependencies
pip install -r requirements.txt

**3. Configure Environment
In a .env file add your Google Gemini API key:
GEMINI_API_KEY=your_actual_api_key_here

**Running the Web Interface
python src/app.py
