from flask import Flask, render_template, request, jsonify
from llm import process_llm_response, process_query

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Get message from request data
    user_message = request.form.get("message")
    user_message = process_query(user_message)

    # Process user message using the chatbot logic
    bot_response = process_llm_response(user_message)

    # Return chatbot response as JSON
    return jsonify(bot_response)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
