import streamlit as st
import pickle 
import pandas as pd 
import requests

def fetch_(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4d96a3c0c6a3e79599957026b888af15'.format(movie_id))
    data = response.json()
    
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity =pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
st.markdown("---")

selected_movie_name =  st.selectbox(
    'Enter movie name',movies['title'].values
)

import streamlit as st

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_cols = 5
    col_width = 120  # Adjust the width of each column as needed

    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction: row;}</style>', unsafe_allow_html=True)
    st.write('<style>div.Widget.row-widget.stRadio > div > label{margin-left: 10px;}</style>', unsafe_allow_html=True)

    for i in range(0, len(names), num_cols):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index = i + j
            if index < len(names):
                with cols[j]:
                    st.image(posters[index], use_column_width=True)
                    st.markdown(f"<p style='text-align:center; width:{col_width}px'>{names[index]}</p>", unsafe_allow_html=True)
