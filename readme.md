# Excel_ChatBot
A Flask app that converts natural language queries into SQL using LangChain and LLaMA (Groq) for querying uploaded Excel files.

## Environment Setup
This project requires an API key to function properly. To keep your API key secure, this project uses environment variables.
## Environment Setup

This project requires Python 3.8+ and an API key to function properly. Follow these steps to set up your environment securely:

### 1. Create a Python virtual environment

It’s best to run the project inside a virtual environment to keep dependencies isolated.

python3 -m venv myenv
source myenv/bin/activate     # On Windows use: myenv\Scripts\activate
### Steps to Set Up
pip install -r requirements.txt


1. **Create the `.env` file**

   Copy the example environment file `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   
2. Add your real API key
Open the .env file in a text editor and replace the placeholder with your actual API key. For example:
API_KEY=your_real_api_key_here
Save the .env file
Run the project

The project will load the API key securely from your .env file.


## Features
- Upload Excel files
- Converts Excel to SQLite
- Use natural language to query the database using LangChain + Groq

## Tech Stack
- Python + Flask
- SQLite
- LangChain + LLaMA (Groq)
