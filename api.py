from flask import request
from src.app import app
from src.config import PORT
import src.controllers.database
from src.controllers import user
from src.controllers import chat

# Welcome to the api

@app.route("/")
def welcome ():
    return "Welcome to API-Project"

# Add users to the DB

@app.route("/user/create/<username>", methods=['GET'])
def create_user(username):
    return user.createUser(username)

#Create a chat

@app.route("/chat/create/<theme>", methods=['GET'])
def create_chat(theme):
    return chat.createChat(theme)

#Add user into a chat

@app.route("/chat/<chat_id>/adduser/<user_id>", methods=['GET'])
def add_user_to_chat(chat_id, user_id):
    return chat.addUser(chat_id, user_id)

#Add messages in a chat

@app.route("/chat/<chat_id>/<user_id>/<message>", methods=['GET'])
def add_message(chat_id, user_id, message):
    return chat.addMessage(chat_id, user_id, message)

#Obtain with all messages from a chat

@app.route('/chat/get/<chat_id>/list', methods=['GET'])
def get_messages(chat_id):
    return chat.getMessages(chat_id)

#Given a username to get a list with the ids

@app.route('/user/get/<username>', methods=['GET'])
def get_ids (username):
    return user.getIds(username)

#Analyze sentiment of the messages in a chat

@app.route('/chat/<chat_id>/sentiment', methods=['GET'])
def sentiment_analyzer(chat_id):
    return chat.sentiment(chat_id)

#Recommend 3 users

@app.route('/user/<user_id>/recommend', methods=['GET'])
def recommend_user(user_id):
    return user.recommendUser(user_id)


app.run("0.0.0.0", PORT, debug=True)
