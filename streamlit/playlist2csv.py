import requests
import csv

def generate_playlist_csv(playlist_id, access_token, output_file="playlist_data.csv"):

    # Base URLs for Spotify API endpoints
    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    audio_features_url = "https://api.spotify.com/v1/audio-features"

    # Headers for authorization
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Initialize a list to hold all track data
    track_data = []

    # Get tracks from the playlist
    print("Fetching playlist tracks...")
    while playlist_url:
        response = requests.get(playlist_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching playlist tracks: {response.json()}")
            return

        playlist_response = response.json()
        for item in playlist_response.get("items", []):
            track = item["track"]
            if track:  # Ensure track is not None
                track_data.append({
                    "track_id": track["id"],
                    "artists": ", ".join(artist["name"] for artist in track["artists"]),
                    "album_name": track["album"]["name"],
                    "track_name": track["name"],
                    "popularity": track["popularity"],
                    "duration_ms": track["duration_ms"],
                    "explicit": track["explicit"]
                })
                print(track["id"])


                # print(audio_features_url + '/' + track['id'])
                # return
                response = requests.get(audio_features_url + '/' + track['id'], headers=headers)
                if response.status_code != 200:
                    print(f"Error fetching audio features: {response.json()}")
                    return

                feature = response.json()
                if feature:  # Ensure feature is not None
                    track.update({
                        "danceability": features.get("danceability"),
                        "energy": features.get("energy"),
                        "key": features.get("key"),
                        "loudness": features.get("loudness"),
                        "mode": features.get("mode"),
                        "speechiness": features.get("speechiness"),
                        "acousticness": features.get("acousticness"),
                        "instrumentalness": features.get("instrumentalness"),
                        "liveness": features.get("liveness"),
                        "valence": features.get("valence"),
                        "tempo": features.get("tempo"),
                        "time_signature": features.get("time_signature"),
                        "track_genre": None  # Placeholder, as genre is not directly available via Spotify API
                    })

        # Check if there is a next page of tracks
        playlist_url = playlist_response.get("next")

    # Write data to CSV
    print(f"Writing data to {output_file}...")
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "track_id", "artists", "album_name", "track_name", "popularity", "duration_ms", "explicit",
            "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo", "time_signature", "track_genre"
        ])
        writer.writeheader()
        writer.writerows(track_data)

    print(f"CSV file generated: {output_file}")

playlist = '15mKRqcixQDZcXkbLHkDtF'
token = # your own token

generate_playlist_csv(playlist, token)