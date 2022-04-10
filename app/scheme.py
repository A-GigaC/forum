# Note: the module name is psycopg, not psycopg3
import psycopg

with psycopg.connect("dbname=test user=postgres") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        cur.execute("SELECT * FROM test")
        cur.fetchone()
        for record in cur:
            print(record)

        conn.commit()