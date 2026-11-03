EXPLAIN ANALYZE
SELECT b.book_id, b.title, a.author_name, b.price
FROM authors AS a
JOIN books AS b ON b.author_id = a.author_id
WHERE a.author_id = 42;
