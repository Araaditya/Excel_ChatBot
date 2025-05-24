import sqlite3
import pandas as pd
import io
import os

DEFAULT_TABLE_NAME = "uploaded_data"

def sanitize_column_names(columns):
    return [col.strip().replace(" ", "_").replace("-", "_").replace("'", "").lower() for col in columns]

def get_connection(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")
    return sqlite3.connect(db_path, check_same_thread=False)

def load_excel_to_sqlite(db_path, excel_file_path, table_name=DEFAULT_TABLE_NAME):
    df = pd.read_excel(excel_file_path)
    df.columns = sanitize_column_names(df.columns)
    conn = get_connection(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    return table_name, list(df.columns)

def get_schema(db_path, table_name=DEFAULT_TABLE_NAME):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns

def export_table_to_excel_memory(db_path, table_name=DEFAULT_TABLE_NAME):
    conn = get_connection(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=table_name)
    output.seek(0)
    return output
