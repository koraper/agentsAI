---
name: sql-optimization-patterns
description: 마스터 SQL 쿼리 최적화, 색인 strategies, 및 EXPLAIN 분석 에 dramatically improve 데이터베이스 성능 및 eliminate slow 쿼리. Use 때 디버깅 slow 쿼리, designing 데이터베이스 스키마, 또는 optimizing 애플리케이션 성능.
---

# SQL 최적화 패턴

Transform slow 데이터베이스 쿼리 into lightning-fast 작업 통해 systematic 최적화, 적절한 색인, 및 쿼리 plan 분석.

## 때 에 Use This Skill

- 디버깅 slow-실행 중 쿼리
- Designing performant 데이터베이스 스키마
- Optimizing 애플리케이션 응답 times
- Reducing 데이터베이스 load 및 costs
- Improving scalability 위한 growing datasets
- Analyzing EXPLAIN 쿼리 계획합니다
- Implementing efficient 인덱스
- 해결하는 N+1 쿼리 문제

## 핵심 개념

### 1. 쿼리 실행 계획합니다 (EXPLAIN)

Understanding EXPLAIN 출력 is 기본 에 최적화.

**PostgreSQL EXPLAIN:**
```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- With actual execution stats
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- Verbose output with more details
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

**키 메트릭 에 Watch:**
- **Seq Scan**: 전체 테이블 scan (일반적으로 slow 위한 large 테이블)
- **인덱스 Scan**: 사용하여 인덱스 (좋은)
- **인덱스 오직 Scan**: 사용하여 인덱스 없이 touching 테이블 (최선의)
- **Nested 루프**: Join 메서드 (okay 위한 small datasets)
- **해시 Join**: Join 메서드 (좋은 위한 larger datasets)
- **Merge Join**: Join 메서드 (좋은 위한 정렬된 데이터)
- **Cost**: 추정 쿼리 cost (lower is 더 나은)
- **행**: 추정 행 returned
- **Actual 시간**: Real 실행 시간

### 2. 인덱스 Strategies

인덱스 are the most 강력한 최적화 tool.

**인덱스 유형:**
- **B-트리**: default, 좋은 위한 equality 및 범위 쿼리
- **해시**: 오직 위한 equality (=) comparisons
- **GIN**: 전체-text search, 배열 쿼리, JSONB
- **GiST**: Geometric 데이터, 전체-text search
- **BRIN**: Block 범위 인덱스 위한 매우 large 테이블 와 함께 correlation

```sql
-- Standard B-Tree index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (index subset of rows)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (include additional columns)
CREATE INDEX idx_users_email_covering ON users(email)
INCLUDE (name, created_at);

-- Full-text search index
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB index
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

### 3. 쿼리 최적화 패턴

**Avoid SELECT \*:**
```sql
-- Bad: Fetches unnecessary columns
SELECT * FROM users WHERE id = 123;

-- Good: Fetch only what you need
SELECT id, email, name FROM users WHERE id = 123;
```

**Use 곳 Clause Efficiently:**
```sql
-- Bad: Function prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: Create functional index or use exact match
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Then:
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Or store normalized data
SELECT * FROM users WHERE email = 'user@example.com';
```

**Optimize 결합합니다:**
```sql
-- Bad: Cartesian product then filter
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id AND u.created_at > '2024-01-01';

-- Good: Filter before join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- Better: Filter both tables
SELECT u.name, o.total
FROM (SELECT * FROM users WHERE created_at > '2024-01-01') u
JOIN orders o ON u.id = o.user_id;
```

## 최적화 패턴

### 패턴 1: Eliminate N+1 쿼리

**문제: N+1 쿼리 Anti-패턴**
```python
# Bad: Executes N+1 queries
users = db.query("SELECT * FROM users LIMIT 10")
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)
    # Process orders
```

**Solution: Use 결합합니다 또는 Batch 로드**
```sql
-- Solution 1: JOIN
SELECT
    u.id, u.name,
    o.id as order_id, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.id IN (1, 2, 3, 4, 5);

-- Solution 2: Batch query
SELECT * FROM orders
WHERE user_id IN (1, 2, 3, 4, 5);
```

```python
# Good: Single query with JOIN or batch load
# Using JOIN
results = db.query("""
    SELECT u.id, u.name, o.id as order_id, o.total
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.id IN (1, 2, 3, 4, 5)
""")

# Or batch load
users = db.query("SELECT * FROM users LIMIT 10")
user_ids = [u.id for u in users]
orders = db.query(
    "SELECT * FROM orders WHERE user_id IN (?)",
    user_ids
)
# Group orders by user_id
orders_by_user = {}
for order in orders:
    orders_by_user.setdefault(order.user_id, []).append(order)
```

### 패턴 2: Optimize Pagination

**나쁜: 오프셋 에 Large 테이블**
```sql
-- Slow for large offsets
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;  -- Very slow!
```

**좋은: Cursor-Based Pagination**
```sql
-- Much faster: Use cursor (last seen ID)
SELECT * FROM users
WHERE created_at < '2024-01-15 10:30:00'  -- Last cursor
ORDER BY created_at DESC
LIMIT 20;

-- With composite sorting
SELECT * FROM users
WHERE (created_at, id) < ('2024-01-15 10:30:00', 12345)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Requires index
CREATE INDEX idx_users_cursor ON users(created_at DESC, id DESC);
```

### 패턴 3: 집계 Efficiently

**Optimize 개수 쿼리:**
```sql
-- Bad: Counts all rows
SELECT COUNT(*) FROM orders;  -- Slow on large tables

-- Good: Use estimates for approximate counts
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'orders';

-- Good: Filter before counting
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';

-- Better: Use index-only scan
CREATE INDEX idx_orders_created ON orders(created_at);
SELECT COUNT(*) FROM orders
WHERE created_at > NOW() - INTERVAL '7 days';
```

**Optimize 그룹 에 의해:**
```sql
-- Bad: Group by then filter
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 10;

-- Better: Filter first, then group (if possible)
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE status = 'completed'
GROUP BY user_id
HAVING COUNT(*) > 10;

-- Best: Use covering index
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

### 패턴 4: Subquery 최적화

**Transform Correlated Subqueries:**
```sql
-- Bad: Correlated subquery (runs for each row)
SELECT u.name, u.email,
    (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count
FROM users u;

-- Good: JOIN with aggregation
SELECT u.name, u.email, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name, u.email;

-- Better: Use window functions
SELECT DISTINCT ON (u.id)
    u.name, u.email,
    COUNT(o.id) OVER (PARTITION BY u.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

**Use CTEs 위한 Clarity:**
```sql
-- Using Common Table Expressions
WITH recent_users AS (
    SELECT id, name, email
    FROM users
    WHERE created_at > NOW() - INTERVAL '30 days'
),
user_order_counts AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT ru.name, ru.email, COALESCE(uoc.order_count, 0) as orders
FROM recent_users ru
LEFT JOIN user_order_counts uoc ON ru.id = uoc.user_id;
```

### 패턴 5: Batch 작업

**Batch INSERT:**
```sql
-- Bad: Multiple individual inserts
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Carol', 'carol@example.com');

-- Good: Batch insert
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Carol', 'carol@example.com');

-- Better: Use COPY for bulk inserts (PostgreSQL)
COPY users (name, email) FROM '/tmp/users.csv' CSV HEADER;
```

**Batch 업데이트:**
```sql
-- Bad: Update in loop
UPDATE users SET status = 'active' WHERE id = 1;
UPDATE users SET status = 'active' WHERE id = 2;
-- ... repeat for many IDs

-- Good: Single UPDATE with IN clause
UPDATE users
SET status = 'active'
WHERE id IN (1, 2, 3, 4, 5, ...);

-- Better: Use temporary table for large batches
CREATE TEMP TABLE temp_user_updates (id INT, new_status VARCHAR);
INSERT INTO temp_user_updates VALUES (1, 'active'), (2, 'active'), ...;

UPDATE users u
SET status = t.new_status
FROM temp_user_updates t
WHERE u.id = t.id;
```

## 고급 Techniques

### Materialized 뷰

Pre-compute expensive 쿼리.

```sql
-- Create materialized view
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
    u.id,
    u.name,
    COUNT(o.id) as total_orders,
    SUM(o.total) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;

-- Add index to materialized view
CREATE INDEX idx_user_summary_spent ON user_order_summary(total_spent DESC);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_order_summary;

-- Concurrent refresh (PostgreSQL)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;

-- Query materialized view (very fast)
SELECT * FROM user_order_summary
WHERE total_spent > 1000
ORDER BY total_spent DESC;
```

### 분할

분할된 large 테이블 위한 더 나은 성능.

```sql
-- Range partitioning by date (PostgreSQL)
CREATE TABLE orders (
    id SERIAL,
    user_id INT,
    total DECIMAL,
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- Queries automatically use appropriate partition
SELECT * FROM orders
WHERE created_at BETWEEN '2024-02-01' AND '2024-02-28';
-- Only scans orders_2024_q1 partition
```

### 쿼리 Hints 및 최적화

```sql
-- Force index usage (MySQL)
SELECT * FROM users
USE INDEX (idx_users_email)
WHERE email = 'user@example.com';

-- Parallel query (PostgreSQL)
SET max_parallel_workers_per_gather = 4;
SELECT * FROM large_table WHERE condition;

-- Join hints (PostgreSQL)
SET enable_nestloop = OFF;  -- Force hash or merge join
```

## 최선의 관행

1. **인덱스 Selectively**: 또한 많은 인덱스 slow down 씁니다
2. **모니터 쿼리 성능**: Use slow 쿼리 로깅합니다
3. **Keep 통계 업데이트된**: Run ANALYZE 정기적으로
4. **Use 적절한 데이터 유형**: Smaller 유형 = 더 나은 성능
5. **Normalize Thoughtfully**: Balance 정규화 vs 성능
6. **캐시 자주 Accessed 데이터**: Use 애플리케이션-레벨 캐싱
7. **연결 풀링**: Reuse 데이터베이스 연결
8. **일반 유지보수**: VACUUM, ANALYZE, rebuild 인덱스

```sql
-- Update statistics
ANALYZE users;
ANALYZE VERBOSE orders;

-- Vacuum (PostgreSQL)
VACUUM ANALYZE users;
VACUUM FULL users;  -- Reclaim space (locks table)

-- Reindex
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
```

## 일반적인 Pitfalls

- **Over-색인**: 각 인덱스 slows down INSERT/업데이트/DELETE
- **Unused 인덱스**: Waste 공간 및 slow 씁니다
- **Missing 인덱스**: Slow 쿼리, 전체 테이블 scans
- **암시적인 유형 변환**: 방지합니다 인덱스 usage
- **또는 Conditions**: Can't use 인덱스 efficiently
- **같은 와 함께 Leading Wildcard**: `LIKE '%abc'` can't use 인덱스
- **함수 에서 곳**: 방지합니다 인덱스 usage 하지 않는 한 기능적인 인덱스 exists

## 모니터링 쿼리

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Find missing indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;

-- Find unused indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## 리소스

- **참조/postgres-최적화-가이드.md**: PostgreSQL-특정 최적화
- **참조/mysql-최적화-가이드.md**: MySQL/MariaDB 최적화
- **참조/쿼리-plan-분석.md**: Deep dive into EXPLAIN 계획합니다
- **자산/인덱스-전략-checklist.md**: 때 및 어떻게 에 create 인덱스
- **자산/쿼리-최적화-checklist.md**: 단계-에 의해-단계 최적화 가이드
- **스크립트/analyze-slow-쿼리.sql**: Identify slow 쿼리 에서 your 데이터베이스
- **스크립트/인덱스-recommendations.sql**: Generate 인덱스 recommendations
