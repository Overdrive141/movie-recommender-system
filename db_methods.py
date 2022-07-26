import streamlit as st
import pickle
from pymongo import MongoClient
import gridfs

client = MongoClient("mongodb+srv://farhan141:PIF5T576k628Wf2v@cluster0.9pefk.mongodb.net/?retryWrites=true&w=majority")
db = client.test
fs = gridfs.GridFS(db) # MongoDB GridFS

# Cached for 3500minutes so query does not run every time I refresh
@st.experimental_memo(ttl=3500)
def get_movies():
    json_data = {}
    movies = db.processed_movies_list.find({'name': 'processedMovieList'})
    for i in movies:
        json_data = i
    pickled_movies = json_data['processedMovieList']
    movies = pickle.loads(pickled_movies)
    return movies

# Cached for 3500minutes so query does not run every time I refresh
@st.experimental_memo(ttl=3500)
def get_similarities():
    # Using GridFS I find all the chunks that were saved from the notebook
    file = fs.find_one({'filename': 'similarities'})
    # Now we read the file and convert it back to original sklearn vector using pickle.loads
    similarityDocument = file.read()
    similarity = pickle.loads(similarityDocument)
    return similarity