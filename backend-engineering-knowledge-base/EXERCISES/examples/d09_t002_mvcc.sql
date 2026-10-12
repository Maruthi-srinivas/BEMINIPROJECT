
-- xmin/xmax on a live row (catalog example)
SELECT ctid, xmin, xmax, * FROM pg_class WHERE relname = 'pg_class' LIMIT 3;
BEGIN;
SELECT txid_current();
ROLLBACK;
