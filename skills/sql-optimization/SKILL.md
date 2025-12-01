---
name: workbench:sql-optimization
description: Optimize SQL queries through EXPLAIN analysis, indexing strategies, and query rewriting. Use when debugging slow queries, designing schemas, or improving database performance.
when_to_use: When queries are slow. When designing database schemas. When seeing sequential scans on large tables. When debugging N+1 query problems. When pagination is slow.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

# SQL Optimization

**Announce at start:** "I'm using the sql-optimization skill to improve query performance."

## Overview

Transform slow queries into fast ones through systematic analysis.

**Core principle:** Understand the query plan before optimizing.

## Quick Reference

| Problem | Solution |
|---------|----------|
| Sequential scan | Add index on WHERE/JOIN columns |
| N+1 queries | Use JOIN or batch IN clause |
| Slow pagination | Cursor-based instead of OFFSET |
| Slow aggregates | Materialized view or covering index |
| Function in WHERE | Functional index or normalize data |

## EXPLAIN Analysis

```sql
-- PostgreSQL: Always start here
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users WHERE email = 'x@example.com';
```

**Red flags in output:**
- `Seq Scan` on large tables
- High `actual time`
- `Rows Removed by Filter` >> rows returned
- `Sort` without index

**Good signs:**
- `Index Scan` or `Index Only Scan`
- `Bitmap Index Scan` for multiple conditions
- `Hash Join` for large joins

## Index Strategies

```sql
-- Standard B-tree (equality, range, sorting)
CREATE INDEX idx_users_email ON users(email);

-- Composite (order matters: equality cols first, then range)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial (index subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering (includes data, avoids table lookup)
CREATE INDEX idx_users_email ON users(email) INCLUDE (name, created_at);

-- Functional (for expressions in WHERE)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
```

## Common Anti-Patterns

### N+1 Queries

```python
# BAD: N+1
for user in users:
    orders = query("SELECT * FROM orders WHERE user_id = ?", user.id)

# GOOD: Single query
query("""
    SELECT u.*, o.* FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id IN (?, ?, ?)
""", user_ids)
```

### Slow OFFSET Pagination

```sql
-- BAD: Slow for large offsets
SELECT * FROM users ORDER BY created_at LIMIT 20 OFFSET 100000;

-- GOOD: Cursor-based
SELECT * FROM users
WHERE created_at < :last_seen_timestamp
ORDER BY created_at DESC
LIMIT 20;
```

### Functions Preventing Index Use

```sql
-- BAD: Can't use index
SELECT * FROM users WHERE LOWER(email) = 'x@example.com';

-- GOOD: Functional index
CREATE INDEX idx_email_lower ON users(LOWER(email));
-- Then same query works fast
```

### SELECT *

```sql
-- BAD: Fetches unnecessary data
SELECT * FROM users WHERE id = 123;

-- GOOD: Only what you need
SELECT id, email, name FROM users WHERE id = 123;
```

## Optimization Patterns

### Batch Operations

```sql
-- BAD: Many round trips
INSERT INTO t VALUES (1); INSERT INTO t VALUES (2);

-- GOOD: Single statement
INSERT INTO t VALUES (1), (2), (3);

-- BETTER: COPY for bulk (PostgreSQL)
COPY t FROM '/tmp/data.csv' CSV;
```

### Subquery to JOIN

```sql
-- BAD: Correlated subquery
SELECT name, (SELECT COUNT(*) FROM orders WHERE user_id = u.id)
FROM users u;

-- GOOD: JOIN with GROUP BY
SELECT u.name, COUNT(o.id)
FROM users u LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

### Materialized Views

```sql
-- Pre-compute expensive aggregations
CREATE MATERIALIZED VIEW user_stats AS
SELECT user_id, COUNT(*) orders, SUM(total) spent
FROM orders GROUP BY user_id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

## Monitoring

```sql
-- Find slow queries (PostgreSQL, requires pg_stat_statements)
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;

-- Find missing indexes
SELECT tablename, seq_scan, idx_scan
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan AND seq_scan > 1000;

-- Find unused indexes
SELECT indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

## Maintenance

```sql
-- Update statistics (run after bulk changes)
ANALYZE users;

-- Reclaim space
VACUUM ANALYZE users;

-- Rebuild bloated index
REINDEX INDEX idx_users_email;
```

## Checklist

Before deploying queries:

- [ ] Run EXPLAIN ANALYZE
- [ ] No sequential scans on large tables
- [ ] Indexes exist for WHERE/JOIN columns
- [ ] No N+1 patterns in application code
- [ ] Pagination uses cursor, not OFFSET
- [ ] SELECT only needed columns
