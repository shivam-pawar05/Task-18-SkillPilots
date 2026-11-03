import os, random
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
cfg = dict(host=os.getenv("DB_HOST","localhost"),
           port=int(os.getenv("DB_PORT","3306")),
           user=os.getenv("DB_USER","root"),
           password=os.getenv("DB_PASSWORD",""))

def main():
    db = os.getenv("DB_NAME", "bookstore_benchmark")
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db}`")
    cur.execute(f"USE `{db}`")
    cur.execute("DROP TABLE IF EXISTS books")
    cur.execute("DROP TABLE IF EXISTS authors")
    cur.execute("""CREATE TABLE authors (
        author_id INT PRIMARY KEY, author_name VARCHAR(100) NOT NULL,
        country VARCHAR(60)) ENGINE=InnoDB""")
    # No FK/index on books.author_id until the benchmark creates it.
    cur.execute("""CREATE TABLE books (
        book_id INT AUTO_INCREMENT PRIMARY KEY, author_id INT NOT NULL,
        title VARCHAR(150) NOT NULL, price DECIMAL(10,2) NOT NULL,
        quantity INT NOT NULL DEFAULT 0) ENGINE=InnoDB""")
    authors = [(i, f"Author {i}", ["India","UK","USA","Canada"][i % 4])
               for i in range(1,101)]
    cur.executemany("INSERT INTO authors VALUES (%s,%s,%s)", authors)
    random.seed(7)
    batch = []
    for i in range(1,50001):
        batch.append((random.randint(1,100), f"Book Title {i}",
                      round(random.uniform(100,1500),2), random.randint(0,100)))
        if len(batch) == 1000:
            cur.executemany("""INSERT INTO books
                (author_id,title,price,quantity) VALUES (%s,%s,%s,%s)""", batch)
            conn.commit()
            batch = []
    if batch:
        cur.executemany("""INSERT INTO books
            (author_id,title,price,quantity) VALUES (%s,%s,%s,%s)""", batch)
        conn.commit()
    cur.execute("ANALYZE TABLE authors, books")
    print("Created bookstore_benchmark: 100 authors, 50,000 books; no author_id index.")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
