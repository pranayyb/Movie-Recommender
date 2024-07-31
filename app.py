# cd movie_recommender
# source myenv/bin/activate

import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="Movie Recommender System", 
    page_icon="🎬",  # Optionally, you can set a custom icon
)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?append_to_response=yes&language=en-US".format(
        movie_id
    )
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4Mzk5ODMyZmY3MWQyYzVlNGEyNDk3NzYzOTMwMjU5OSIsIm5iZiI6MTcyMTkwNDgzNy43Mjk3NTMsInN1YiI6IjY2YTIyYzhiOWU3NWZkZDBjOTI2NjU4ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ls7mdS6R7Wkagkz6i87kygvVe0NUoHd483fyosBa1vA",
    }
    response = requests.get(url, headers=headers)
    # data = requests.get(url)
    data = response.json()
    # st.text(data)
    poster_path = data["poster_path"]
    # st.text(poster_path)
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # st.text(full_path)
    return full_path


def recommend(movie):
    movie_index = movies_list_df[movies_list_df["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies_list_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_list_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_list_df = pickle.load(open("movies.pkl", "rb"))
movies_list = movies_list_df["title"].values
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommender System")
option = st.selectbox("Select a Movie: ", movies_list)

if st.button("Recommend"):
    names, posters = recommend(option)
    st.write("Recommended Movies:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.write(names[0])
    with col2:
        st.image(posters[1])
        st.write(names[1])
    with col3:
        st.image(posters[2])
        st.write(names[2])
    with col4:
        st.image(posters[3])
        st.write(names[3])
    with col5:
        st.image(posters[4])
        st.write(names[4])
