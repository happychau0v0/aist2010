import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import streamlit.components.v1 as components
import ollama  # Import the ollama package to query the API

st.set_page_config(page_title="Spotify Song Recommendation")

# Load the track dataset
@st.cache
def load_data():
    df = pd.read_csv("dataset4.csv")  # Load the new dataset
    df['track_genre'] = df['track_genre'].apply(lambda x: [i.strip() for i in str(x).split(",")])  # Assuming genres are comma-separated
    exploded_track_df = df.explode('track_genre')  # Explode the genre column
    return exploded_track_df

exploded_track_df = load_data()

# Get a list of all unique genres
all_genres = sorted(exploded_track_df['track_genre'].unique())  # Updated to use 'track_genre'
print(all_genres)
audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]

# Helper function to query the ollama API
def query_ollama(image_path):
    response = ollama.chat(
        model='music',
        messages=[{
            'role': 'user',
            'content': 'Here is the image. Focus solely on analyzing the image and describing the music that would fit with the visual style, without interpreting or addressing any personal emotional or psychological states.',
            'images': [image_path]  # Send the image to ollama for analysis
        }]
    )
    
    # Parse the response from ollama
    content = response['message']['content']
    music_attributes = {}
    print(content)
    for line in content.split('\n'):
        if line:  # Skip empty lines
            key, value = line.split(':', 1)
            music_attributes[key.strip()] = value.strip()

    # Return parsed music attributes
    return music_attributes

# Nearest neighbors function for recommendations
def n_neighbors_uri_audio(genre, test_feat):
    genre = genre.lower()
    genre_data = exploded_track_df[(exploded_track_df["track_genre"] == genre)]
    genre_data = genre_data.sort_values(by='popularity', ascending=False)[:500]

    if len(genre_data) == 0:  # If no data matches the query
        return [], []

    neigh = NearestNeighbors()
    neigh.fit(genre_data[audio_feats].to_numpy())

    n_neighbors = neigh.kneighbors([test_feat], n_neighbors=len(genre_data), return_distance=False)[0]
    track_ids = genre_data.iloc[n_neighbors]["track_id"].tolist()  # Updated to use 'track_id'
    audios = genre_data.iloc[n_neighbors][audio_feats].to_numpy()
    return track_ids, audios

# Streamlit UI
title = "Spotify Song Recommendation Engine :33"
st.title(title)

# Initialize session state for multi-step process
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # Start at step 1 (Upload Image)

if 'music_attributes' not in st.session_state:
    st.session_state['music_attributes'] = None

# Step 1: Upload Image
if st.session_state['step'] == 1:
    st.markdown("### Step 1: Upload an image to detect emotions")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        img_path = f"./images/uploaded_{uploaded_file.name}"
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Move to step 2 (Wait for analysis)
        st.session_state['step'] = 2
        st.session_state['img_path'] = img_path

# Step 2: Wait for Analysis
if st.session_state['step'] == 2:
    st.markdown("### Step 2: Waiting for analysis...")
    st.markdown("This is running on my Macbook so it might take some time >_<")
    
    # Simulate waiting by analyzing the image
    img_path = st.session_state['img_path']
    with st.spinner('Analyzing your image...'):
        music_attributes = query_ollama(img_path)
    
    # Store the music attributes in session state and move to step 3
    st.session_state['music_attributes'] = music_attributes
    st.session_state['step'] = 3

# Step 3: Tuning and Song Recommendations
if st.session_state['step'] == 3:
    st.markdown("### Step 3: Customize tuning and get song recommendations")
    st.markdown("The result is here, but please feel free to change the values!")
    
    # Extract music attributes from session state
    music_attributes = st.session_state['music_attributes']
    
    # Use the returned music attributes from ollama
    acousticness = float(music_attributes['acousticness'])
    danceability = float(music_attributes['danceability'])
    energy = float(music_attributes['energy'])
    instrumentalness = float(music_attributes['instrumentalness'])
    liveness = float(music_attributes['liveness'])
    loudness = float(music_attributes['loudness'])
    speechiness = float(music_attributes['speechiness'])
    valence = float(music_attributes['valence'])
    tempo = float(music_attributes['tempo'])
    genre = music_attributes['genre']

    # Collapsible section for customizing features
    with st.expander("Customize Features (Optional)", expanded=False):
        # UI for users to further customize the features
        # Use a searchable dropdown (selectbox) for genres
        genre = st.selectbox("Choose your genre:", all_genres, index=all_genres.index(genre))
        acousticness = st.slider('Acousticness', 0.0, 1.0, acousticness)
        danceability = st.slider('Danceability', 0.0, 1.0, danceability)
        energy = st.slider('Energy', 0.0, 1.0, energy)
        instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, instrumentalness)
        liveness = st.slider('Liveness', 0.0, 1.0, liveness)
        loudness = st.slider('Loudness', -60.0, 0.0, loudness)
        speechiness = st.slider('Speechiness', 0.0, 1.0, speechiness)
        valence = st.slider('Valence', 0.0, 1.0, valence)
        tempo = st.slider('Tempo', 30.0, 244.0, tempo)

    # Create a row of buttons: one for "Search for Recommendations" and another for "Select Another Image"
    col1, col2 = st.columns([1, 1])

    # Button to search for recommendations
    with col1:
        search_button = st.button('Search for Recommendations')

    # Button to select another image
    with col2:
        select_image_button = st.button('Select Another Image')

    if select_image_button:
        # Reset to step 1 to allow another image upload
        st.session_state['step'] = 1
        st.session_state['music_attributes'] = None
        st.session_state['img_path'] = None
        st.experimental_rerun()

    if search_button:
        # Generate recommendations
        test_feat = [acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]
        track_ids, audios = n_neighbors_uri_audio(genre, test_feat)

        # Handle no results case
        if not track_ids:
            st.warning("No songs found matching your search criteria. Please try adjusting the parameters.")
        else:
            tracks_per_page = 6
            tracks = []
            for track_id in track_ids:
                track = f"""<iframe src="https://open.spotify.com/embed/track/{track_id}" width="260" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>"""
                tracks.append(track)

            if 'previous_inputs' not in st.session_state:
                st.session_state['previous_inputs'] = [genre] + test_feat

            current_inputs = [genre] + test_feat
            if current_inputs != st.session_state['previous_inputs']:
                if 'start_track_i' in st.session_state:
                    st.session_state['start_track_i'] = 0
                st.session_state['previous_inputs'] = current_inputs

            if 'start_track_i' not in st.session_state:
                st.session_state['start_track_i'] = 0

            with st.container():
                col1, col2, col3 = st.columns([2, 1, 2])
                if st.button("Recommend More Songs"):
                    if st.session_state['start_track_i'] < len(tracks):
                        st.session_state['start_track_i'] += tracks_per_page
                current_tracks = tracks[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
                current_audios = audios[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
                if st.session_state['start_track_i'] < len(tracks):
                    for i, (track, audio) in enumerate(zip(current_tracks, current_audios)):
                        if i % 2 == 0:
                            with col1:
                                components.html(track, height=400)  
                        else:
                            with col3:
                                components.html(track, height=400)
                else:
                    st.write("No songs left to recommend!")
