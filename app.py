from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, flash

from logic import logic_blueprint
from db import get_connection, get_schema, load_excel_to_sqlite
from auth import auth_blueprint

app = Flask(__name__)
app.secret_key = 'API_KEY'

app.register_blueprint(logic_blueprint)
app.register_blueprint(auth_blueprint)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
db_path = 'uploaded_excel.db'


@app.route('/', methods=['GET', 'POST'])
def login():
    from auth import USER_CREDENTIALS  # Import from centralized auth

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USER_CREDENTIALS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if not os.path.exists(db_path):
        flash("No data available. Please upload an Excel file first.")
        return redirect(url_for('upload'))

    try:
        conn = get_connection(db_path)
        df = pd.read_sql_query("SELECT * FROM uploaded_data", conn)
        conn.close()
        return render_template('dashboard.html', username=session['username'], role=session['role'], tables=[df.to_html(classes='dataframe')])
    except Exception:
        flash("Error reading from database.")
        return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['excel_file']
        if file and file.filename.endswith(('.xls', '.xlsx')):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            load_excel_to_sqlite(db_path, filepath)
            flash('File uploaded and loaded into SQLite')
            return redirect(url_for('dashboard'))
        flash('Invalid file format')
    return render_template('upload.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'username' not in session:
        return redirect(url_for('login'))

    result = None
    generated_sql = None

    if request.method == 'POST':
        from langchain_utils import get_sql_chain
        user_question = request.form['nl_query']
        try:
            schema = get_schema(db_path)
            sql_chain = get_sql_chain(schema)
            query_text = sql_chain.invoke({"question": user_question}).content.strip()
            conn = get_connection(db_path)
            df = pd.read_sql_query(query_text, conn)
            conn.close()
            result = df.to_html(classes='dataframe')
            generated_sql = query_text
        except Exception as e:
            result = f"<p style='color:red;'>Error: {e}</p>"

    return render_template('query.html', result=result, generated_sql=generated_sql)


@app.route('/logout')
def logout():
    uploaded_file = session.get('uploaded_file')
    if uploaded_file and os.path.exists(uploaded_file):
        os.remove(uploaded_file)

    uploaded_db = session.get('db_path')
    if uploaded_db and os.path.exists(uploaded_db):
        os.remove(uploaded_db)

    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
