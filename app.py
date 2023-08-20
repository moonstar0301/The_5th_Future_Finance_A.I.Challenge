from flask import Flask, render_template, request, jsonify
from llm import process_llm_response, q_generator, mindmap_generator
from database import database_generator
import os

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = 'your_api_key'

# Generating vector database
vectordb = database_generator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    
    # Process user message using both logic
    bot_response = process_llm_response(user_message, vectordb)
    subject, contents = mindmap_generator(vectordb, user_message)
    
    mind_map_flag = 1 # 마인드맵 버튼 활성화 여부
    if not subject and not contents:
#        bot_response += ' with empty list'
        mind_map_flag = 0 # 마인드맵 불가능이면 비활성화
    
    # Return combined response as JSON화
    response_data = {
        "bot_response": bot_response,
        "subject": subject,
        "contents": contents,
        "mind_map_flag": mind_map_flag
    }

    return jsonify(response_data)

# Recommended Question generator
@app.route("/qgenerator", methods=["POST"])
def qgenerator():

    bot_recommend = []
    bot_recommend = q_generator(vectordb)
    # Return chatbot response as JSON
    return jsonify(bot_recommend)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
