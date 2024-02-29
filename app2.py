# import required functions, classes
import re
from autollm import AutoQueryEngine
from autollm.utils.document_reading import read_files_as_documents
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import threading

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Use the environment variable as needed
os.environ["OPENAI_API_KEY"] = openai_api_key

# Read files as documents
required_exts = [".pdf"]
documents = read_files_as_documents(input_dir="evaDocs", required_exts=required_exts)

# Initialize AutoQueryEngine
query_engine = AutoQueryEngine.from_defaults(documents=documents)

# Dictionary to store chat messages by user
chat_memory = {}

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('query')
    response = query_engine.query(user_input).response
    
    # Store user input in chat memory
    user = request.json.get('user')
    if user not in chat_memory:
        chat_memory[user] = []
    chat_memory[user].append(user_input)
    
    return jsonify({"response": response})

@app.route('/chat_memory', methods=['GET'])
def get_chat_memory():
    user = request.args.get('user')
    if user in chat_memory:
        return jsonify({"chat_memory": chat_memory[user]})
    else:
        return jsonify({"chat_memory": []})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

