import os
import json
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mall_segmentation")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():

    if not DB_PASSWORD:
        raise ValueError(
            "DB_PASSWORD environment variable is not set."
        )

    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

    return connection


def test_connection():

    connection = get_connection()

    try:

        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                "SELECT version();"
            )

            result = cursor.fetchone()

            return result

    finally:

        connection.close()


def create_upload(filename, total_rows):

    connection = get_connection()

    try:

        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            query = """
                INSERT INTO uploads (
                    filename,
                    total_rows,
                    status
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                RETURNING upload_id, filename, total_rows, status, uploaded_at;
            """

            cursor.execute(
                query,
                (
                    filename,
                    total_rows,
                    "uploaded",
                ),
            )

            result = cursor.fetchone()

            connection.commit()

            return result

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()

def insert_raw_rows(upload_id, dataframe):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            query = """
                INSERT INTO raw_customer_data (
                    upload_id,
                    row_number,
                    raw_data
                )
                VALUES (
                    %s,
                    %s,
                    %s
                );
            """

            for index, row in dataframe.iterrows():

                raw_data = {}

                for column, value in row.items():

                    if pd.isna(value):
                        raw_data[column] = None
                    else:
                        raw_data[column] = value

                cursor.execute(
                    query,
                    (
                        upload_id,
                        index + 1,
                        json.dumps(raw_data),
                    ),
                )

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()

def log_error(
    error_type,
    error_message,
    endpoint=None,
    upload_id=None,
):

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            query = """
                INSERT INTO error_logs (
                    error_type,
                    error_message,
                    endpoint,
                    upload_id
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                );
            """

            cursor.execute(
                query,
                (
                    error_type,
                    error_message,
                    endpoint,
                    upload_id,
                ),
            )

        connection.commit()

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()

def save_error_to_database(
    error_message,
    error_traceback,
):
    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            query = """
                INSERT INTO error_logs (
                    error_message,
                    error_traceback
                )
                VALUES (
                    %s,
                    %s
                );
            """

            cursor.execute(
                query,
                (
                    error_message,
                    error_traceback,
                ),
            )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()