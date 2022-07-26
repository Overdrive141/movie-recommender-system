import streamlit as st
import pandas as pd
import requests
from pymongo import MongoClient
import gridfs
from db_methods import get_similarities, get_movies

movies = get_movies()
similarity = get_similarities()

### Old Methods. Replaced by GridFS & MongoDB Find in Real Time
# movies = pickle.load(open('processed_movie_list.pkl','rb'))
# similarity = pickle.load(open('similarity.pkl','rb'))

st.header('MongoDB Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

apiUrl = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"


def fetch_movie_details(movie_id):
    url = apiUrl.format(movie_id)
    data = requests.get(url)
    data = data.json()
    # st.write(data)
    # poster_path = data['poster_path']
    return data

def fetch_poster(movie_id):
    url = apiUrl.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    # st.write(poster_path)
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommendMovie(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    movie_details = fetch_movie_details(movies.iloc[distances[0][0]].movie_id)
    for i in distances[0:6]:
        # fetch the movie poster

        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters,movie_details

if st.button('Search Movie'):

    recommended_movie_names,recommended_movie_posters,movie_details = recommendMovie(selected_movie)

    colName, colPoster = st.columns([1, 2]) # 1 col take 1 part 2nd col takes 3 parts

    with colName:
        st.image(recommended_movie_posters[0])
    with colPoster:
        st.subheader(recommended_movie_names[0])
        genre = []
        for genres in movie_details['genres']:
            genre.append(genres['name'])
        st.caption(f"Genre: {', '.join(genre)} | Released: {movie_details['release_date']}")
        st.write(movie_details['overview'])
        st.text(f"TMDB Rating: {round(movie_details['vote_average'], 1)}")
        st.progress(float(movie_details['vote_average'])/10)

    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.subheader("Similar to what you searched")

    col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])



    with col1:
        st.image(recommended_movie_posters[1])
        st.markdown(recommended_movie_names[1])

    with col2:
        st.image(recommended_movie_posters[2])
        st.markdown(recommended_movie_names[2])

    with col3:
        st.image(recommended_movie_posters[3])
        st.markdown(recommended_movie_names[3])

    with col4:
        st.image(recommended_movie_posters[4])
        st.markdown(recommended_movie_names[4])

    with col5:
        st.image(recommended_movie_posters[5])
        st.markdown(recommended_movie_names[5])

