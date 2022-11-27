import requests
from bs4 import BeautifulSoup
import pprint

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

"""this part of the code was run and the txt file with songs was created"""
# URL = f"https://www.billboard.com/charts/hot-100/{date}/"
#
# response = requests.get(url=URL)
# soup = BeautifulSoup(response.text, "html.parser")
#
# songs = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only", id="title-of-a-story")
# top_bilboard = soup.find(name="a", class_="c-title__link lrv-a-unstyle-link").getText().strip()
# songs_list = [song.getText().strip() for song in songs]
# songs_list.insert(0, top_bilboard)
#
# # print(songs_list)
# # print(len(songs_list))
#
# with open("songs.txt", "a", encoding="utf-8") as f:
#     for i in range(len(songs_list)):
#         text = songs_list[i] +"\n"
#         f.write(text)


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = sp.search("Call Me Maybe")
# uri = results["tracks"]["items"]
# pprint.pprint(results["tracks"]["items"][0]["uri"])

uri_list = []

with open("songs.txt", 'r', encoding='utf-8') as f:
    data = f.read().splitlines()
    for song in data:
        results = sp.search(song)
        uri = results["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
#
# with open("songs_uri.txt", 'a', encoding='utf-8') as f:
#     for uri in uri_list:
#         text = uri + "\n"
#         f.write(text)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://localhost:8888/callback/",
        client_id="get_your_client_id_at_spotify_api",
        client_secret= "get_your_client_secret_at_spotify_api",
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = ["The list of", "song URIs", "you got by", "searching Spotify"]

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)