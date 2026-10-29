
import os
import psycopg
from psycopg.rows import dict_row

database_url = os.environ.get("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is not set.")

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1,
    )

with psycopg.connect(
    database_url,
    row_factory=dict_row,
    connect_timeout=10,
) as connection:
    rows = connection.execute(
        """
        SELECT
            id,
            full_name,
            CASE
                WHEN qr_token IS NULL OR qr_token = '' THEN 'MISSING'
                ELSE 'PRESENT'
            END AS token_status
        FROM visitors
        ORDER BY id
        """
    ).fetchall()

    print("Visitor count:", len(rows))

    for row in rows:
        print(
            f"ID: {row['id']} | "
            f"Name: {row['full_name']} | "
            f"QR token: {row['token_status']}"
        )
