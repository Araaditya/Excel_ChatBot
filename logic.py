from flask import Blueprint, request, jsonify, send_file
from db import load_excel_to_sqlite, get_schema, export_table_to_excel_memory, get_connection
from langchain_utils import get_sql_chain
import pandas as pd

logic_blueprint = Blueprint('logic', __name__)
db_path = "uploaded_excel.db"

@logic_blueprint.route('/upload_excel', methods=['POST'])
def upload_excel():
    file = request.files['file']
    file.save(file.filename)
    table_name, _ = load_excel_to_sqlite(db_path, file.filename)
    return jsonify({"message": "File uploaded and loaded into DB", "table": table_name})

@logic_blueprint.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.json['question']
    schema = get_schema(db_path)
    sql_chain = get_sql_chain(schema)
    sql_response = sql_chain.invoke({"question": question}).content.strip()
    return jsonify({"query": sql_response})

@logic_blueprint.route('/run_query', methods=['POST'])
def run_query():
    query = request.json['query']
    conn = get_connection(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_json(orient='records')

@logic_blueprint.route('/export_excel', methods=['GET'])
def export_excel():
    output = export_table_to_excel_memory(db_path)
    return send_file(output, as_attachment=True, download_name="updated_file.xlsx")
