# Note: the module name is psycopg, not psycopg3
import psycopg

with psycopg.connect("postgresql://root@localhost:5432/forum?password=root") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            drop database users;
        """)

        # cur.execute("""
        #     CREATE TABLE users (
        #         id serial PRIMARY KEY,
        #         nickname text,
        #         password text
        #     );
        #     CREATE TABLE profiles (
        #         id serial PRIMARY KEY,
        #         name text,
        #         user_id int not null,
        #         constraint fk_user foreign key(user_id) references user(id)
        #     );
        # """)

        # cur.execute(
        #     "INSERT INTO users (nickname, password) VALUES (%s, %s)",
        #     ("aboba", "14ilove88pizza228"),
        #     "INSERT INTO forums (nickname, name) VALUES (%s, %s)",
        #     ("aboba", "anton")
        # )

        # cur.execute("SELECT * FROM test")
        # for record in cur:
        #     print(record)

        conn.commit()

# def sign_in(login, password):

# def sign_up(login, password, name):

# if (__name__ == '__main__'):
