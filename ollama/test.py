import ollama

# Simulating the response object after querying the API
response = ollama.chat(
    model='music',
    messages=[{
        'role': 'user',
        'content': '',
        'images': ['image.jpg']
    }]
)

# Extract the content string from the response
content = response['message']['content']

# Split the content into individual lines and parse them into a dictionary
music_attributes = {}
for line in content.split('\n'):
    if line:  # skip empty lines
        key, value = line.split(':', 1)  # Split only on the first colon
        music_attributes[key.strip()] = value.strip()

# Now, the music_attributes dictionary contains all the attributes
print(music_attributes)

# Access individual attributes
acousticness = float(music_attributes['acousticness'])
danceability = float(music_attributes['danceability'])
energy = float(music_attributes['energy'])
instrumentalness = float(music_attributes['instrumentalness'])
liveness = float(music_attributes['liveness'])
loudness = float(music_attributes['loudness'])
speechiness = float(music_attributes['speechiness'])
valence = float(music_attributes['valence'])
tempo = float(music_attributes['tempo'])  # This is a string like '110-120 BPM'
release_year = music_attributes['release_year']  # This is a string like '2015-2020'
genre = music_attributes['genre']  # This is a string like 'Pop'

# Print the variables
print(f"Acousticness: {acousticness}")
print(f"Danceability: {danceability}")
print(f"Energy: {energy}")
print(f"Instrumentalness: {instrumentalness}")
print(f"Liveness: {liveness}")
print(f"Loudness: {loudness}")
print(f"Speechiness: {speechiness}")
print(f"Valence: {valence}")
print(f"Tempo: {tempo}")
print(f"Release Year: {release_year}")
print(f"Genre: {genre}")