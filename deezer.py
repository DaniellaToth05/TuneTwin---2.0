import requests

def get_artwork(song, artist):
    base_url = "https://api.deezer.com/search"

    query = f'track:"{song}" artist:"{artist}"'
    response = requests.get(base_url, params={"q": query})

    if response.status_code == 200:
        data = response.json()
        if data["data"]:  # Check if results are returned
            track_info = data["data"][0]  # Get the first result
            album_cover_url = track_info["album"]["cover_big"]  # Album artwork URL
            return album_cover_url
        else: 
            return None
    else:
        return None