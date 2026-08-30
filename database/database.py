import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def create_message(message: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (message)
                VALUES (%s)
                RETURNING id;
                """,
                (message,),
            )
            message_id = cursor.fetchone()[0]

    return message_id


def get_messages():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, message
                FROM messages
                ORDER BY id;
                """)
            rows = cursor.fetchall()

    return rows


def update_message(message_id: int, message: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE messages
                SET message = %s
                WHERE id = %s
                RETURNING id;
                """,
                (message, message_id),
            )
            row = cursor.fetchone()

    return row is not None


def delete_message(message_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM messages
                WHERE id = %s
                RETURNING id;
                """,
                (message_id,),
            )
            row = cursor.fetchone()

    return row is not None
