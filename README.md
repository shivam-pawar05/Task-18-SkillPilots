# Bookstore Query Performance Benchmark

Compares a books/authors JOIN query before and after indexing `books.author_id`.

## Requirements
- MySQL 8.0.18+ (EXPLAIN ANALYZE support)
- Python 3.9+
- MySQL user allowed to create databases, tables, and indexes

## Run
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and set your MySQL credentials.
3. `python scripts/setup_db.py`
4. `python scripts/benchmark.py`

Setup creates database `bookstore_benchmark`, 100 authors, and 50,000 books.
The benchmark column intentionally has no foreign key/index initially, allowing a
valid before/after comparison. The script saves plans and timings in `results/`.

Run only on a test database. Timings depend on hardware, cache, MySQL version, and data.
