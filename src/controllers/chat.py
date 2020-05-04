from src.controllers.database import db
from src.controllers.errorHandler import APIError, Error404, errorHandler
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
chat = db["chat"]
users = db["user"]

@errorHandler
def createChat(chatname):
    myquery = list(chat.find({'Theme': chatname }, {'_id':0}))
    if myquery:
        raise APIError(f'Chat {chatname} already exists')
    x = chat.insert_one({'Theme': chatname, 'users':[], 'messages':[]})
    chat_id = x.inserted_id
    return dumps([chat_id, {'Theme':chatname}])

@errorHandler
def addUser(chat_id, user_id):
    myquery = list(chat.find({'_id':ObjectId(chat_id)}, {'_id':0}))
    if not myquery:
        raise APIError (f'The chat {chat_id} does not exist, please create a new chat or try a different chat_id')
    if user_id in myquery[0]['users']:
        raise APIError(f'User: {user_id} already exists')
    chat.update({'_id':ObjectId(chat_id)}, {"$push":{'users':user_id}})
    return dumps (f'User {user_id} add to chat {ObjectId(chat_id)}')

@errorHandler
def addMessage(chat_id, user_id, message):
    myquery = list(chat.find({'_id':ObjectId(chat_id)}, {'_id':0}))
    if not myquery:
        raise APIError (f'The chat {chat_id} does not exist, please create a new chat or try a different chat_id')
    if user_id not in myquery[0]['users']:
        addUser(chat_id, user_id)
    chat.update({'_id':ObjectId(chat_id)}, {"$push":
    {'messages':
    {'message_id': ObjectId(),
    'user_id': user_id,
    'text': message,
    'time': datetime.datetime.now()}}})
    return dumps (f'Message sent correctly to chat {chat_id} at {datetime.datetime.now()}')

@errorHandler
def getMessages (chat_id):
    myquery = list(chat.find({'_id':ObjectId(chat_id)}, {'_id':0}))
    if not myquery:
        raise APIError('Chat not found')
    return dumps(myquery[0]['messages'])

def sentiment (chat_id):
    messages = list(chat.find({'_id':ObjectId(chat_id)}, {'_id':0})[0]['messages'])
    sentiment=[]
    for m in messages:
        info={}
        info['message'] = m['text']
        info['time']=  m['time']
        info['user_id'] = m['user_id']
        sia = SentimentIntensityAnalyzer()
        info['sentiment'] = sia.polarity_scores(m['text'])
        sentiment.append(info)
    return dumps(sentiment)

    


