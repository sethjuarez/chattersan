import re
import os
import json
import logging
from flask import Flask, request
from flask_cors import CORS
from oai import OpenAI, Context
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='[%m/%d/%Y %I:%M:%S %p]',
                    level=logging.INFO)

logging.info("Starting server...")
logging.info(f"API_TYPE: {os.getenv('API_TYPE') or '[EMPTY]'}")
logging.info(f"API_BASE: {os.getenv('API_BASE') or '[EMPTY]'}")
logging.info(f"API_VERSION: {os.getenv('API_VERSION') or '[EMPTY]'}")
logging.info(f"API_KEY: {len(os.getenv('API_KEY')) * '*' if  os.getenv('API_KEY') != None else '[EMPTY]'}")
logging.info(f"ORIGINS: {os.getenv('ORIGINS') or '[EMPTY]'}")


app = Flask(__name__)
cors = CORS(app, resources={r"/chat/*": {"origins": (os.getenv("ORIGINS") or '*').split(",")}})


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/chat", methods=["POST"])
def chat():
    # Message format
    # {
    #     "question": "What is GitHub?",
    #     "context": [
    #         {     
    #             "question": "Hello, who are you?",
    #             "answer": "Hi there! I am a GitHub AI assistant here to answer your questions."
    #         } 
    #     ] 
    # }
    # Context is optional but helps OAI to understand the context of the conversation (if needed)
    # question is required

    data = request.get_json()
    logging.info(f"Received request:\n{json.dumps(data, indent=4)}\n")
    prompt = data['question']
    context = []
    if 'context' in data:
        context = data['context']
        context = [Context(c['question'], c['answer']) for c in context]
    
    oai = OpenAI()
    
    r = oai.chat(prompt, context)
    logging.info(f"Response:\n{json.dumps(r, indent=4)}\n")
    
    return r


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
