import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.header('Movie Similarity Analysis')
movies = pickle.load(open('processed_movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))



movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown to get cosine similarity analysis",
    movie_list
)

apiUrl = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

def recommendMovie(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    similarity_number = []

    for i in distances[0:50]:
        # fetch the movie poster
        recommended_movie_names.append(movies.iloc[i[0]].title)
        similarity_number.append(i[1])

    return recommended_movie_names,similarity_number

if st.button('Search Movie'):

    recommended_movie_names,similarity_number = recommendMovie(selected_movie)

    similarity_number=np.array(similarity_number)
    recommended_movie_names=np.array(recommended_movie_names)

    df = pd.DataFrame({'Movie Name': list(recommended_movie_names), 'Cosine Similarity Value': list(similarity_number)})
    # colName = st.columns(5) # 1 col take 1 part 2nd col takes 3 parts

    # with

    with st.container():
        df = df.set_index('Movie Name')
        st.line_chart(df, use_container_width=False, width=900, height=500)

    df=df.reset_index()
    df.index = np.arange(1, len(df)+1)

    st.write("This is inside the container")
    st.table(df)





