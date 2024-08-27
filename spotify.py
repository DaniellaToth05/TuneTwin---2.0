from dotenv import load_dotenv
import os
import base64
import json
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_song(token, song, artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"track:{song} artist:{artist}"
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        json_result = json.loads(response.content)["tracks"]["items"]

        if len(json_result) == 0:
            print("Song or artist not found...")
            return None

        return json_result[0]

    else:
        return{"error": "Unable to fetch data from Spotify"}

def get_recs(token, seed_tracks, seed_artists=None, seed_genres=None, limit=25, market='CA'):

    url = "https://api.spotify.com/v1/recommendations"
    headers = get_auth_header(token)

    params = {
        "seed_tracks": seed_tracks,
        "limit": limit,
        "market": market
    }

    if seed_artists:
        params["seed_artists"] = seed_artists
    if seed_genres:
        params["seed_genres"] = seed_genres

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        recommendations = response.json()
        return recommendations
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

# token = get_token()
# search_results = search_for_song(token, "not like us", "kendick lamar")
# if search_results is None:
#     pass
# else:
#     track_id = search_results["id"]
#     recommendations = get_recs(token, track_id)
#     tracks = recommendations.get('tracks', [])
#     for track in tracks:
#         track_name = track.get('name')
#         track_url = track.get('external_urls', {}).get('spotify')
#         artists = [artist.get('name') for artist in track.get('artists', [])]
#         artist_names = ", ".join(artists)

#         print(f"Track Name: {track_name}")
#         print(f"Artists: {artist_names}")
#         print(f"Spotify URL: {track_url}")
#         print("-" * 40)