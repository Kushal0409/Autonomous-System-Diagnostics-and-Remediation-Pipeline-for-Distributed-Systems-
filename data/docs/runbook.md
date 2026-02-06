# Engineering Runbook: Database Connection Issues

## Error: ConnectionPoolTimeoutError
**Symptoms:** - API returns 500 status codes.
- Logs show "Timeout waiting for connection from pool".
- Latency spikes on endpoints /api/v1/users.

## Root Causes
1. **Traffic Spike:** Sudden increase in concurrent users exceeding `MAX_CONNECTIONS`.
2. **Zombie Connections:** Application not closing connections properly (missing `.close()` or `try/finally` blocks).
3. **Database Maintenance:** DB is undergoing patches or backups.

## Remediation Steps
1. **Immediate Mitigation:** Restart the application service (`sudo systemctl restart api-service`) to flush the pool.
2. **Investigation:** Check `pg_stat_activity` for idle transactions.
3. **Long-term Fix:** Increase `MAX_CONNECTIONS` in `config.yaml` or implement connection pooling proxy (PgBouncer).