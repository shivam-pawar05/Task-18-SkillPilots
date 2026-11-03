import os, time, csv
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
cfg = dict(host=os.getenv("DB_HOST","localhost"),
           port=int(os.getenv("DB_PORT","3306")),
           user=os.getenv("DB_USER","root"),
           password=os.getenv("DB_PASSWORD",""),
           database=os.getenv("DB_NAME","bookstore_benchmark"))
query = """EXPLAIN ANALYZE
SELECT b.book_id, b.title, a.author_name, b.price
FROM authors a JOIN books b ON b.author_id = a.author_id
WHERE a.author_id = 42"""

def measure(cur, label):
    start = time.perf_counter()
    cur.execute(query)
    plan = "\\n".join(str(row[0]) for row in cur.fetchall())
    elapsed = (time.perf_counter() - start) * 1000
    print(f"\\n--- {label} ---\\n{plan}")
    print(f"Client-side EXPLAIN ANALYZE duration: {elapsed:.3f} ms")
    return plan, elapsed

def main():
    os.makedirs("results", exist_ok=True)
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    before, t_before = measure(cur, "BEFORE INDEX")
    cur.execute("CREATE INDEX idx_books_author_id ON books(author_id)")
    cur.execute("ANALYZE TABLE books")
    after, t_after = measure(cur, "AFTER INDEX")
    for filename, plan, elapsed in [
        ("before_index.txt", before, t_before), ("after_index.txt", after, t_after)]:
        with open(os.path.join("results", filename), "w", encoding="utf-8") as f:
            f.write(plan + f"\\n\\nClient-side duration: {elapsed:.3f} ms\\n")
    with open("results/comparison.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["stage", "client_side_explain_duration_ms"])
        w.writerow(["before_index", f"{t_before:.3f}"])
        w.writerow(["after_index", f"{t_after:.3f}"])
    print("\\nSaved plans and comparison in results/. Compare actual plan operators too.")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
