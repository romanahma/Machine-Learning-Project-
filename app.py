import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch the poster URL from TMDb
def fetch_poster(movie_id):
    api_key = '987ac4f50ba889f66070bcbd2d06ef6b'  # Your TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    # Make an API request to TMDb to get the movie details
    response = requests.get(url)

    # Parse the response to get the poster path
    data = response.json()
    poster_path = data['poster_path']

    # Construct the full URL for the poster image
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    # Get the recommended movies and their posters
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Get the movie ID
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))  # Fetch the poster using the movie ID

    return recommended_movies, recommended_posters


# Load the movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set up the Streamlit app
st.title('Movie Recommender System')

# Create a dropdown for movie selection
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# Show recommendations when the button is clicked
if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(selected_movie_name)

    # Create a single row with multiple columns for each recommended movie
    cols = st.columns(len(recommended_movies))

    for i, col in enumerate(cols):
        with col:
            # Use HTML and JavaScript to make the image clickable
            st.markdown(
                f"""
                <div style="text-align: center; margin: 10px;">
                    <a href="{recommended_posters[i]}" target="_blank">
                        <img src="{recommended_posters[i]}" style="width: 150px; border-radius: 10px; border: 2px solid #ddd;" />
                    </a>
                    <p style="margin-top: 8px; font-weight: bold;">{recommended_movies[i]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
