from flask import Flask, render_template, request, jsonify
from llm import get_source_document_metadata, process_llm_response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get message from request data
    query = request.form.get("message")
    
    # Get response from OpenAI  model
    response = process_llm_response(qa_chain(query))
    
    # Return chatbot response
    return render_template("index.html", user_message=query, bot_response=response)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
