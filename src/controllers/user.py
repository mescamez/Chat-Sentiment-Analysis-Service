from src.controllers.database import db
from src.controllers.errorHandler import APIError, Error404, errorHandler
from bson.json_util import dumps
from bson.objectid import ObjectId
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import numpy as np
users = db["users"]
chat = db['chat']

@errorHandler
def createUser(username):
    myquery = list(users.find({'username':username}, {'_id':0}))
    if myquery:
        raise APIError(f'username {username} already exists')
    x = users.insert_one({'username':username})
    return dumps([x.inserted_id, {'username':username}])

def getIds (username):
    myquery = list(users.find({'username': username}))
    return dumps(myquery[0]['_id'])

def getInfo(user_id):
    chats = list(chat.find({'messages.user_id':user_id}))
    chat_list = []
    for c in chats:
        for n in c['messages']:
            chat_list.append(n)
    return (chat_list)

def recommendUser (user_id):
    chat_list = getInfo(user_id)
    df = pd.DataFrame(chat_list)
    df.drop(['message_id', 'time'], axis=1, inplace=True)
    message_users = df.groupby(['user_id']).agg({'text':'sum'})
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(message_users['text'])
    m = sparse_matrix.todense()
    doc_term_matrix = sparse_matrix.todense()
    df_2 = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=message_users.T.columns)
    similarity_matrix = distance (df_2,df_2)
    sim_df = pd.DataFrame(similarity_matrix, columns=message_users.T.columns, index=message_users.T.columns)
    rec_user_id = sim_df[user_id].sort_values(ascending=False)[1:4]
    rec=list(zip(rec_user_id.index,rec_user_id))
    return dumps(rec)