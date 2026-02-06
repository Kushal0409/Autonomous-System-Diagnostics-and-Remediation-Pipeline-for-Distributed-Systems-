# Post-Incident Report: API 500 Errors on User Service

**Incident ID:** INC-2024-001
**Report Date:** 2024-10-24
**Author:** Technical Operations Team

---

## 1. Executive Summary

On October 24, 2024, at approximately 14:30 UTC, a P1 incident was triggered due to widespread `500 Internal Server Errors` affecting the User Service API. This directly impacted customer login functionality, rendering users unable to access the platform. Monitoring dashboards immediately reported a significant spike in 500 error rates.

Investigation quickly correlated the error spike with database connection pool exhaustion and hard connection acquisition failures within the User Service. The root cause was identified as an unexpected **Traffic Spike**, which overwhelmed the configured database `MAX_CONNECTIONS`. Immediate remediation involved restarting the affected application service to clear the connection pool and restore service. Long-term solutions include increasing the application's `MAX_CONNECTIONS` or implementing a dedicated connection pooling proxy like PgBouncer to enhance resilience against future traffic surges.

---

## 2. Root Cause

The most likely root cause for Incident INC-2024-001 was a **Traffic Spike** that led to the exhaustion of the database connection pool for the User Service.

**Detailed Reasoning:**

*   **Sudden Onset:** At 14:30 UTC, monitoring observed an abrupt and significant increase in 500 Internal Server Errors from the User Service API.
*   **Log Analysis:** Concurrently, application logs revealed numerous "database connection pool exhaustion" and "hard connection acquisition failure" entries, along with "Timeout waiting for connection from pool."
*   **Correlation with Runbook:** These symptoms directly align with the documented behavior for database connection issues, specifically the `ConnectionPoolTimeoutError`, as outlined in the `Engineering Runbook: Database Connection Issues`.
*   **Primary Cause Identified:** The runbook lists "Traffic Spike: Sudden increase in concurrent users exceeding `MAX_CONNECTIONS`" as a primary root cause for such errors. Given the sudden and impactful nature of the event, with no evidence pointing to zombie connections or database maintenance, a surge in user traffic is the most fitting explanation for overwhelming the existing connection capacity.

**Citing Runbook Section:**
`# Engineering Runbook: Database Connection Issues` -> `## Error: ConnectionPoolTimeoutError` -> `## Root Causes` -> `1. Traffic Spike: Sudden increase in concurrent users exceeding MAX_CONNECTIONS.`

---

## 3. Remediation Taken/Suggested

### 3.1. Immediate Remediation Taken

1.  **Application Service Restart:**
    *   To quickly mitigate the `500 Internal Server Errors` and restore service, the `api-service` instances responsible for the User Service were immediately restarted.
    *   **Action:** Executed `sudo systemctl restart api-service` on affected servers.
    *   **Result:** This action successfully cleared the existing database connection pool, closed any potentially stuck connections, and allowed the application to re-establish a fresh set of connections. Service availability for the User Service was restored shortly after the restart.

### 3.2. Post-Incident Investigation (Verification)

1.  **Check `pg_stat_activity`:**
    *   After the service restart, a quick check of the PostgreSQL `pg_stat_activity` view was performed to ensure no lingering "zombie connections" or unusually long-running transactions were present that might contribute to future connection issues.
    *   **Action:** Query executed:
        ```sql
        SELECT datname, pid, usename, application_name, client_addr, backend_start, state, wait_event_type, wait_event, query
        FROM pg_stat_activity
        WHERE datname = 'your_database_name'
        ORDER BY state, backend_start DESC;
        ```
    *   **Result:** The activity looked normal post-restart, confirming the primary issue was indeed resource contention during the traffic spike rather than persistent connection mismanagement.

### 3.3. Long-Term Remediation Suggested

To prevent recurrence of similar incidents caused by traffic spikes exceeding database connection capacity, the following long-term solutions are suggested:

1.  **Increase `MAX_CONNECTIONS` in Application Configuration:**
    *   **Description:** The most direct approach is to increase the `MAX_CONNECTIONS` parameter within the User Service application's configuration. This will allow the application to maintain a larger pool of open database connections, accommodating higher concurrent user loads.
    *   **Action:** Modify the application's `config.yaml` (or equivalent) to increase `database.max_connections` to a value suitable for anticipated peak traffic. This change will require a controlled application restart.
    *   **Consideration:** This should be done carefully, considering the database server's overall capacity and resource limits to avoid overwhelming the database itself.

2.  **Implement a Dedicated Connection Pooling Proxy (e.g., PgBouncer):**
    *   **Description:** For robust and scalable connection management, especially in high-traffic environments, implementing a dedicated connection pooling proxy (such as PgBouncer) between the User Service application and the PostgreSQL database is highly recommended. PgBouncer effectively multiplexes connections, allowing many application connections to share a smaller, fixed number of database connections. This significantly reduces the overhead on the database and improves performance under high load.
    *   **Action:** Plan and execute the architectural change to introduce PgBouncer into the service architecture. This is a more involved change requiring careful planning, configuration, and testing.