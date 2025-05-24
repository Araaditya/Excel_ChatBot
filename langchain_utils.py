from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

def get_sql_chain(schema):
    template = f"""
        You are an expert data analyst. Generate a valid SQL query to answer user questions using the database schema below.
        Only use the table 'uploaded_data'.
        Schema: {schema}

        Rules:
        1. Output ONLY the SQL query.
        2. No explanations.
        3. Syntax must be valid SQLite.
        4. Use LOWER() for comparisons.
        5. Use LIKE '%keyword%' for partial matches.
        6. If it's a yes/no question, respond "Yes" or "No" after checking.
        7. If irrelevant, reply: "Sorry, I can't answer that question based on the provided data."

        User Question: {{question}}
        SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    return prompt | llm
