import os
from tools import read_log_file, read_ticket_data, read_runbook
from agents import IncidentAgents

def main():
    # 1. Setup Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_dir, "data", "logs", "server_logs.txt")
    ticket_path = os.path.join(base_dir, "data", "tickets", "incident_ticket.json")
    runbook_path = os.path.join(base_dir, "data", "docs", "runbook.md")

    # 2. Load Data (The "Input" Phase)
    print("---  STARTING AUTOMATED INCIDENT RESPONSE---")
    logs = read_log_file(log_path)
    ticket = read_ticket_data(ticket_path)
    runbook = read_runbook(runbook_path)

    if not logs or not ticket or not runbook:
        print(" Error: Missing data files.")
        return

    # 3. Initialize Agents
    try:
        agents = IncidentAgents()
    except ValueError as e:
        print(f" Configuration Error: {e}")
        return

    # 4. Agent Workflow Execution
    
    # Step A: Analyze Logs
    log_analysis = agents.log_analysis_agent(logs)
    print(f"\n--- Log Analysis ---\n{log_analysis}\n")

    # Step B: Correlate with Ticket
    correlation = agents.incident_correlator_agent(ticket, log_analysis)
    print(f"\n--- Correlation ---\n{correlation}\n")

    # Step C: Determine Root Cause
    rca = agents.root_cause_agent(correlation, runbook)
    print(f"\n--- Root Cause Analysis ---\n{rca}\n")

    # Step D: Suggest Resolution
    resolution = agents.resolution_agent(rca, runbook)
    print(f"\n--- Suggested Resolution ---\n{resolution}\n")

    # Step E: Generate Final Report
    final_report = agents.report_agent(ticket, rca, resolution)
    
    # 5. Output
    print("\n" + "="*50)
    print(" FINAL POST-INCIDENT REPORT")
    print("="*50)
    print(final_report)
    
    # Save report to file
    with open("post_incident_report.md", "w") as f:
        f.write(final_report)
    print("\n Report saved to post_incident_report.md")

if __name__ == "__main__":
    main()