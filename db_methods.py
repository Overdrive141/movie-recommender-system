import streamlit as st
import pickle
from pymongo import MongoClient
import gridfs
import dns
import certifi

ca = certifi.where()

# client = MongoClient("mongodb+srv://farhan141:PIF5T576k628Wf2v@cluster0.9pefk.mongodb.net")

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    conn = MongoClient(
        "mongodb://farhan141:PIF5T576k628Wf2v@cluster0-shard-00-00.9pefk.mongodb.net:27017,cluster0-shard-00-01.9pefk.mongodb.net:27017,cluster0-shard-00-02.9pefk.mongodb.net:27017/?ssl=true&replicaSet=atlas-gw5a40-shard-0&authSource=admin&retryWrites=true&w=majority",
        tlsCAFile=ca)
    return conn


client = init_connection()


# Cached for 3500minutes so query does not run every time I refresh
@st.experimental_memo(ttl=3500)
def get_movies():
    json_data = {}
    db = client.test
    movies = db.processed_movies_list.find({'name': 'processedMovieList'})
    for i in movies:
        json_data = i
    pickled_movies = json_data['processedMovieList']
    movies = pickle.loads(pickled_movies)
    return movies

# Cached for 3500minutes so query does not run every time I refresh
@st.experimental_memo(ttl=3500)
def get_similarities():
    db = client.test
    fs = gridfs.GridFS(db)  # MongoDB GridFS
    # Using GridFS I find all the chunks that were saved from the notebook
    file = fs.find_one({'filename': 'similarities'})
    # Now we read the file and convert it back to original sklearn vector using pickle.loads
    similarityDocument = file.read()
    similarity = pickle.loads(similarityDocument)
    return similarity