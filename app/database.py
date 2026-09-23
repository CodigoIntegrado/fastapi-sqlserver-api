import os

import pyodbc
from dotenv import load_dotenv


load_dotenv()


DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_DRIVER = os.getenv("DB_DRIVER")


def get_connection():
    connection_string = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)


def test_connection():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                DB_NAME() AS database_name,
                @@SERVERNAME AS server_name,
                GETDATE() AS server_date
        """)

        row = cursor.fetchone()

        return {
            "connected": True,
            "database": row.database_name,
            "server": row.server_name,
            "server_date": row.server_date.isoformat(),
        }

    except Exception as error:
        return {
            "connected": False,
            "error": str(error),
        }

    finally:
        if connection:
            connection.close()