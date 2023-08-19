from flask import Flask, render_template, request, jsonify
from llm import process_llm_response, q_generator, mindmap_generator
from database import database_generator
import os

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = 'my_api_key'

# Generating vector database
vectordb = database_generator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get message from request data
    user_message = request.form.get("message")

    # Process user message using the chatbot logic
    bot_response = process_llm_response(user_message,vectordb)

    # Return chatbot response as JSON
    return jsonify(bot_response)

# MindMap Question generator. 수정필요 
@app.route("/chat", methods=["POST"])
def mgenerator():
    user_message = request.form.get("message")
    small_subject = []
    contents = []
    small_subject, contents = mindmap_generator(vectordb, user_message)
    # Return chatbot response as JSON
    return jsonify(small_subject, contents)


# Recommended Question generator. 수정필요 
@app.route("/qgenerator", methods=["POST"])
def qgenerator():

    bot_response = []
    bot_response = q_generator(vectordb)
    # Return chatbot response as JSON
    return jsonify(bot_response)



# Run the app
if __name__ == "__main__":
    app.run(debug=True)
