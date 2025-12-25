"""
Docstring for db
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "dbname": "finance_pipeline",
    "user": "finance_user",
    "password": "finance_pass",
    "port": 5432
}

def connect_to_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        raise RuntimeError(f"Error connecting to database: {e}") from e

def initialize_db():
    connection = connect_to_db()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                       id SERIAL PRIMARY KEY,
                       file_name TEXT UNIQUE NOT NULL,
                       bank TEXT,
                       processed boolean DEFAULT FALSE,
                       processed_at TIMESTAMP)""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                day INTEGER,
                month TEXT,
                merchant TEXT,
                amount DECIMAL NOT NULL,
                file_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       
                CONSTRAINT fk_file
                    FOREIGN KEY(file_id)
                        REFERENCES files(id)
                        ON DELETE CASCADE
            );
        """)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        connection.close()

def insert_file(file_name, bank=None):
    with connect_to_db() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO files (file_name, bank)
            VALUES (%s, %s)
            RETURNING id
            """,
            (file_name, bank)
        )
        return cur.fetchone()[0]


def insert_transactions(file_id, transactions):
    with connect_to_db() as conn, conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO transactions (day, month, merchant, amount, file_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [
                (
                    t["day"],
                    t["month"],
                    t["merchant"],
                    t["amount"].replace(",", "."),
                    file_id
                )
                for t in transactions
            ]
        )


def mark_file_processed(file_id):
    with connect_to_db() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE files
            SET processed = TRUE,
                processed_at = NOW()
            WHERE id = %s
            """,
            (file_id,)
        )

def file_exists(file_name):
    with connect_to_db() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, processed
            FROM files
            WHERE file_name = %s
            """,
            (file_name,)
        )
        return cur.fetchone()


def transfer_db_to_file(table_name, output_file):
    query = str(sql.SQL("SELECT * FROM {}").format(
        sql.Identifier(table_name)
    ))

    conn = connect_to_db()
    df = pd.read_sql(query, conn)
    conn.close()

    df.to_excel(output_file, index=False)
