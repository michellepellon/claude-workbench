---
name: workbench:sql-db-design
description: SQL database schema design best practices - data types, constraints, indexing, JSONB, and common patterns. Focuses on PostgreSQL but principles apply broadly. Use when designing tables, choosing data types, or setting up constraints.
when_to_use: When designing database schemas. When choosing data types. When adding constraints or indexes. When using JSONB. When partitioning large tables.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash
---

# SQL Database Design

**Announce at start:** "I'm using the sql-db-design skill for schema design."

## Overview

Design PostgreSQL schemas that are correct, performant, and maintainable.

**Core principle:** Normalize first, denormalize only when measured performance requires it.

## Quick Reference: Data Types

| Use Case | Type | Notes |
|----------|------|-------|
| IDs | `BIGINT GENERATED ALWAYS AS IDENTITY` | UUID only if distributed/opaque needed |
| Strings | `TEXT` | Not VARCHAR(n) - use CHECK for limits |
| Money | `NUMERIC(p,s)` | Never float |
| Timestamps | `TIMESTAMPTZ` | Never TIMESTAMP without timezone |
| Booleans | `BOOLEAN NOT NULL` | Unless tri-state needed |
| JSON | `JSONB` | Not JSON (unless order matters) |

### Avoid These Types

```sql
-- DON'T                    -- DO
timestamp                   timestamptz
char(n), varchar(n)         text
money                       numeric
serial                      bigint generated always as identity
```

## Core Rules

1. **Primary keys**: `BIGINT GENERATED ALWAYS AS IDENTITY` for most tables
2. **Foreign keys**: Always add explicit index on FK columns (not auto-created!)
3. **NOT NULL**: Add everywhere semantically required
4. **Naming**: `snake_case`, unquoted (avoids case sensitivity issues)

## Constraints

```sql
-- Primary key (auto-creates index)
user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY

-- Foreign key (must manually add index!)
user_id BIGINT NOT NULL REFERENCES users(user_id)
CREATE INDEX ON orders(user_id);  -- Don't forget this

-- Unique (auto-creates index, allows multiple NULLs)
email TEXT NOT NULL UNIQUE

-- Unique with single NULL (PG15+)
UNIQUE (email) NULLS NOT DISTINCT

-- Check constraint
status TEXT NOT NULL CHECK (status IN ('pending', 'active', 'closed'))
price NUMERIC NOT NULL CHECK (price > 0)
```

## Index Types

| Type | Use For |
|------|---------|
| B-tree (default) | Equality, range, ORDER BY |
| GIN | JSONB, arrays, full-text search |
| GiST | Ranges, geometry, exclusion |
| BRIN | Very large time-series tables |

```sql
-- Composite (leftmost prefix must be in WHERE)
CREATE INDEX ON orders(user_id, created_at);

-- Partial (index subset of rows)
CREATE INDEX ON users(email) WHERE status = 'active';

-- Expression (must match exactly in queries)
CREATE INDEX ON users(LOWER(email));

-- Covering (avoids table lookup)
CREATE INDEX ON users(email) INCLUDE (name);
```

## JSONB

```sql
-- Column with GIN index
attrs JSONB NOT NULL DEFAULT '{}'
CREATE INDEX ON profiles USING GIN(attrs);

-- Query patterns that use GIN index
WHERE attrs @> '{"status": "active"}'  -- containment
WHERE attrs ? 'premium'                 -- key exists

-- Extract scalar for B-tree index (faster for equality/range)
price INT GENERATED ALWAYS AS ((attrs->>'price')::INT) STORED
CREATE INDEX ON products(price);
```

## Common Patterns

### Users Table

```sql
CREATE TABLE users (
  user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT users_email_unique UNIQUE (email)
);
CREATE INDEX ON users(LOWER(email));  -- Case-insensitive lookup
CREATE INDEX ON users(created_at);
```

### Orders with FK

```sql
CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'paid', 'shipped', 'canceled')),
  total NUMERIC(10,2) NOT NULL CHECK (total > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON orders(user_id);      -- FK index (required!)
CREATE INDEX ON orders(created_at);
CREATE INDEX ON orders(status) WHERE status = 'pending';  -- Partial
```

## Partitioning

Use for very large tables (>100M rows) with consistent filter on partition key.

```sql
-- Range partitioning by time
CREATE TABLE events (
  event_id BIGINT GENERATED ALWAYS AS IDENTITY,
  created_at TIMESTAMPTZ NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_q1 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

**Limitation**: PK/UNIQUE must include partition key.

## PostgreSQL Gotchas

| Gotcha | Solution |
|--------|----------|
| FK columns not auto-indexed | Always add index manually |
| Unquoted names lowercased | Use snake_case, avoid quotes |
| UNIQUE allows multiple NULLs | Use `NULLS NOT DISTINCT` (PG15+) |
| Sequence gaps after rollback | Normal - don't try to fix |
| Updates leave dead tuples | VACUUM handles it; avoid wide-row churn |

## Useful Extensions

| Extension | Use For |
|-----------|---------|
| `pg_trgm` | Fuzzy text search, `LIKE '%x%'` |
| `pgcrypto` | Password hashing, UUIDs |
| `timescaledb` | Time-series automation |
| `postgis` | Geospatial |
| `pgvector` | Vector similarity (embeddings) |

## Related Skills

- **sql-optimization**: Query performance, EXPLAIN analysis, N+1 fixes
