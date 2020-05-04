from flask import request
from src.app import app
from src.config import PORT
import src.controllers.database
from src.controllers import user
from src.controllers import chat

@app.route("/user/create/<username>", methods=['GET'])
def create_user(username):
    return user.createUser(username)

@app.route("/chat/create/<theme>", methods=['GET'])
def create_chat(theme):
    return chat.createChat(theme)

@app.route("/chat/<chat_id>/adduser/<user_id>", methods=['GET'])
def add_user_to_chat(chat_id, user_id):
    return chat.addUser(chat_id, user_id)

@app.route("/chat/<chat_id>/<user_id>/<message>", methods=['GET'])
def add_message(chat_id, user_id, message):
    return chat.addMessage(chat_id, user_id, message)

@app.route('/chat/get/<chat_id>/list', methods=['GET'])
def get_messages(chat_id):
    return chat.getMessages(chat_id)

@app.route('/user/get/<username>', methods=['GET'])
def get_ids (username):
    return user.getIds(username)

@app.route('/chat/<chat_id>/sentiment', methods=['GET'])
def sentiment_analyzer(chat_id):
    return chat.sentiment(chat_id)

@app.route('/user/<user_id>/recommend', methods=['GET'])
def recommend_user(user_id):
    return user.recommendUser(user_id)


app.run("0.0.0.0", PORT, debug=True)
