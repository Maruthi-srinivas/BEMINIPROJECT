-- D09-T001: architecture introspection
SELECT pid, backend_type, state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE backend_type IS NOT NULL
ORDER BY backend_type, pid;

SHOW max_connections;
SHOW shared_buffers;
