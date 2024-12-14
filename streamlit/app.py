import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit.components.v1 as components
import ollama

st.set_page_config(page_title="Spotify Song Recommendation :D")

# Load the track dataset
@st.cache
def fetch_dataset():
    track_data = pd.read_csv("dataset4.csv")
    track_data['track_category'] = track_data['track_genre'].apply(lambda x: [i.strip() for i in str(x).split(",")])
    expanded_track_data = track_data.explode('track_category')

    # Normalize loudness and tempo using their specific ranges
    expanded_track_data['loudness'] = (expanded_track_data['loudness'] + 60) / 60
    expanded_track_data['tempo'] = (expanded_track_data['tempo'] - 60) / 180

    return expanded_track_data

track_data_expanded = fetch_dataset()

# Get a list of all unique genres
unique_genres = sorted(track_data_expanded['track_category'].unique())
audio_features = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]

# Helper function to query the ollama API
def api_query_ollama(image_loc):
    api_response = ollama.chat(
        model='music',
        messages=[{
            'role': 'user',
            'content': 'Here is the image. Focus solely on analyzing the image and describing the music that would fit with the visual style, without interpreting or addressing any personal emotional or psychological states.',
            'images': [image_loc]
        }]
    )
    
    message_content = api_response['message']['content']
    audio_attributes = {}
    for line in message_content.split('\n'):
        if line:
            key, value = line.split(':', 1)
            audio_attributes[key.strip()] = value.strip()

    return audio_attributes

# Nearest neighbors function for recommendations
def find_similar_tracks(selected_genre, input_features):
    input_features[-4] = (input_features[-4] + 60) / 30
    input_features[-1] = (input_features[-1] - 60) / 90

    genre_filtered_data = track_data_expanded[(track_data_expanded["track_category"] == selected_genre)]
    genre_filtered_data = genre_filtered_data.sort_values(by='popularity', ascending=False)[:20]

    if len(genre_filtered_data) == 0:
        return [], []

    neighbor_model = NearestNeighbors()
    neighbor_model.fit(genre_filtered_data[audio_features].to_numpy())

    neighbors = neighbor_model.kneighbors([input_features], n_neighbors=len(genre_filtered_data), return_distance=False)[0]
    track_identifiers = genre_filtered_data.iloc[neighbors]["track_id"].tolist()
    audio_data = genre_filtered_data.iloc[neighbors][audio_features].to_numpy()
    return track_identifiers, audio_data

# Streamlit UI
app_title = "Spotify Song Recommendation Engine :33"
st.title(app_title)

# Initialize session state for multi-step process
if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 1

if 'detected_audio_attributes' not in st.session_state:
    st.session_state['detected_audio_attributes'] = None

if 'recommended_tracks' not in st.session_state:
    st.session_state['recommended_tracks'] = ([], [])

# Add a session state flag to reset the file uploader
if 'reset_file_uploader' not in st.session_state:
    st.session_state['reset_file_uploader'] = False

st.markdown("### Step 0 (optional): Generate Playlist CSV from Playlist ID")
input_playlist_id = st.text_input("Enter your Spotify Playlist ID:")
input_access_token = st.text_input("Enter your Spotify Access Token:", type="password")  # Token input

if st.button("Generate Playlist CSV"):
    st.error("Sadly, Spotify has disabled track audio features API since Nov 27. (https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api)")

# Step 1: Upload Image
st.markdown("### Step 1: Upload an image to detect emotions")

# Reset the uploader if the user clicks "Select Another Image"
if st.session_state['reset_file_uploader']:
    st.session_state.clear()
    st.session_state['current_step'] = 1
    st.session_state['reset_file_uploader'] = False
    st.experimental_rerun()

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image_location = f"./images/uploaded_{uploaded_image.name}"
    with open(image_location, "wb") as f:
        f.write(uploaded_image.getbuffer())
    
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    st.session_state['image_location'] = image_location
    st.session_state['current_step'] = max(st.session_state['current_step'], 2)

# Step 2: Wait for Analysis
if st.session_state.get('current_step', 1) >= 2:
    st.markdown("### Step 2: Waiting for analysis...")
    st.markdown("This is running on my Macbook so it might take some time >_<")
    
    if st.session_state['current_step'] == 2:
        image_location = st.session_state['image_location']
        with st.spinner('Analyzing your image...'):
            detected_attributes = api_query_ollama(image_location)
        
        st.session_state['detected_audio_attributes'] = detected_attributes
        st.session_state['current_step'] = 3

# Step 3: Tuning and Song Recommendations
if st.session_state.get('current_step', 1) >= 3:
    st.markdown("### Step 3: Customize tuning and get song recommendations")
    st.markdown("The result is here, but please feel free to change the values!")
    
    detected_attributes = st.session_state['detected_audio_attributes']

    acousticness = float(detected_attributes['acousticness'])
    danceability = float(detected_attributes['danceability'])
    energy = float(detected_attributes['energy'])
    instrumentalness = float(detected_attributes['instrumentalness'])
    liveness = float(detected_attributes['liveness'])
    loudness = float(detected_attributes['loudness'])
    speechiness = float(detected_attributes['speechiness'])
    valence = float(detected_attributes['valence'])
    tempo = float(detected_attributes['tempo'])
    genre = detected_attributes['genre']

    with st.expander("Customize Features (Optional)", expanded=False):
        genre = st.selectbox("Choose your genre:", unique_genres, index=unique_genres.index(genre))
        acousticness = st.slider('Acousticness', 0.0, 1.0, acousticness)
        danceability = st.slider('Danceability', 0.0, 1.0, danceability)
        energy = st.slider('Energy', 0.0, 1.0, energy)
        instrumentalness = st.slider('Instrumentalness', 0.0, 1.0, instrumentalness)
        liveness = st.slider('Liveness', 0.0, 1.0, liveness)
        loudness = st.slider('Loudness', -60.0, 0.0, loudness)
        speechiness = st.slider('Speechiness', 0.0, 1.0, speechiness)
        valence = st.slider('Valence', 0.0, 1.0, valence)
        tempo = st.slider('Tempo', 60.0, 240.0, tempo)

    col1, col2 = st.columns([1, 1])

    with col1:
        search_button = st.button('Search for Recommendations')
        if search_button:
            input_features = [acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]
            recommended_track_ids, recommended_audios = find_similar_tracks(genre, input_features)
            st.session_state['recommended_tracks'] = (recommended_track_ids, recommended_audios)

    with col2:
        select_new_image_button = st.button('Select Another Image')
        if select_new_image_button:
            # Set reset_file_uploader to True and restart the app
            st.session_state['reset_file_uploader'] = True
            st.experimental_rerun()

    # Display recommendations
    recommended_track_ids, recommended_audios = st.session_state['recommended_tracks']
    if recommended_track_ids:
        tracks_per_page = 6  # Number of tracks to show per page
        track_frames = []
        for track_id in recommended_track_ids:
            track_frame = f"""
                <div style="display: flex; justify-content: center;">
                    <iframe src="https://open.spotify.com/embed/track/{track_id}" width="280" height="540" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                </div>
                """
            track_frames.append(track_frame)

        if 'start_track_index' not in st.session_state:
            st.session_state['start_track_index'] = 0

        with st.container():
            if st.button("Recommend More Songs"):
                if st.session_state['start_track_index'] < len(track_frames):
                    st.session_state['start_track_index'] += tracks_per_page
            
            current_frames = track_frames[st.session_state['start_track_index']: st.session_state['start_track_index'] + tracks_per_page]
            current_audios = recommended_audios[st.session_state['start_track_index']: st.session_state['start_track_index'] + tracks_per_page]
            
            if st.session_state['start_track_index'] < len(track_frames):
                for track_frame, audio_data in zip(current_frames, current_audios):
                    # Use a single column for each track
                    with st.container():
                        components.html(track_frame, height=400)
            else:
                st.write("No songs left to recommend!")