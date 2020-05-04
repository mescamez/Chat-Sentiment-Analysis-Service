# Chat-Sentiment-Analysis-Service

The aim of this project is to create an API in Flask in order to generate conversations between different users in a chat. In the SRC folder, a folder called controllers could be find, with different files with the necessary code to implement the API.

- api.py: File which connect the API and the endpoints created.
- user.py: code to insert the users in the users collection and to obtain the corresponding ids
- chat.py: code to create chats, add users into a specific chat, write messages of a specific user in a certain chat, obtain a list of messages and analyze this messages.
- errorhandler.py: function to control possible errors when making requests to the API.

## API endpoints

### 1. User endpoints

* (GET) /user/create/<username>

- Purpose: Create an user and save it into DB
- Params: username
- Returns: user_id and username

* (GET) /user/get/<username>

- Purpose: Given a username, obtain the corresponding id
- Paramas: Username
- Returns: An array of ids

* (GET) /user/<user_id>/recommend

- Purpose: Recommend friend to this user based on chat contents
- Paramas: user_id
- Returns: json array with top 3 similar users

### 2. Chat endpoints:

* (GET) /chat/create/<theme>

- Purpose: Create a conversation to load messages
- Params: The theme of the chat (chatname)
- Returns: chat_id and chatname

* (GET) /chat/<chat_id>/adduser/<user_id>

- Purpose: Add a user or a list of users to a chat
- Params: chat_id and user_id
- Returns: 'User {user_id} add to chat {ObjectId(chat_id)}

* (GET) /chat/<chat_id>/<user_id>/<message>

- Purpose: Add a message to the conversation
- Params: chat_id, user_id and text
- Returns: 'Message sent correctly to the chat {chat_id} at {datetime.datetime.now()}

* (GET) /chat/get/<chat_id>/list

- Purpose: Get all messages from chat_id
- Returns: json array with all messages from this chat_id

* (GET) /chat/<chat_id>/sentiment

- Purpose: Analyze messages from chat_id using NLTK sentiment analysis package
- Returns: json with all sentiments from messages in the chat
