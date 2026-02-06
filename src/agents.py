import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables
load_dotenv()

class IncidentAgents:
    def __init__(self):
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        
        # We use Gemini 1.5 Flash for speed and efficiency
        self.model_name = "gemini-2.5-flash" 

    def _call_llm(self, role_description, user_content):
        """Helper to call Gemini API"""
        
        # Initialize the model with a system instruction (Role)
        model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=role_description
        )
        
        # Generate content
        try:
            response = model.generate_content(user_content)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {e}"

    # --- AGENT 1: Log Analyst ---
    def log_analysis_agent(self, logs):
        print("🔎 Log Analysis Agent Working...")
        role = """
        You are a Senior Site Reliability Engineer (SRE).
        Your task is to analyze server logs. 
        Identify patterns of errors, timestamps of failure start, and specific error messages.
        Output a concise summary of the anomalies found.
        """
        return self._call_llm(role, f"Analyze these logs:\n{logs}")

    # --- AGENT 2: Incident Correlator ---
    def incident_correlator_agent(self, ticket, log_analysis):
        print("🔗 Incident Correlator Agent Working...")
        role = """
        You are an Incident Commander.
        Correlate the user-reported incident ticket with the technical log analysis.
        Confirm if the logs support the ticket description.
        """
        content = f"Ticket:\n{ticket}\n\nLog Analysis:\n{log_analysis}"
        return self._call_llm(role, content)

    # --- AGENT 3: Root Cause Analyst (RCA) ---
    def root_cause_agent(self, correlation_findings, runbook):
        print("🧠 Root Cause Agent Working...")
        role = """
        You are a Root Cause Analysis Expert.
        Using the incident correlation and the provided Engineering Runbook, determine the most likely root cause.
        Cite the specific section of the runbook that matches the symptoms.
        """
        content = f"Findings:\n{correlation_findings}\n\nRunbook:\n{runbook}"
        return self._call_llm(role, content)

    # --- AGENT 4: Resolution Agent ---
    def resolution_agent(self, root_cause_analysis, runbook):
        print("🛠️ Resolution Agent Working...")
        role = """
        You are a DevOps Automation Engineer.
        Based on the identified root cause and the runbook, generate a step-by-step remediation plan.
        If the runbook has specific commands, include them.
        """
        content = f"RCA:\n{root_cause_analysis}\n\nRunbook Content:\n{runbook}"
        return self._call_llm(role, content)

    # --- AGENT 5: Report Generator ---
    def report_agent(self, ticket, rca, resolution):
        print("📝 Report Agent Working...")
        role = """
        You are a Technical Writer.
        Generate a professional Post-Incident Report (PIR) in Markdown format.
        Include:
        1. Executive Summary
        2. Root Cause
        3. Remediation Taken/Suggested
        """
        content = f"Ticket: {ticket}\nRCA: {rca}\nResolution: {resolution}"
        return self._call_llm(role, content)