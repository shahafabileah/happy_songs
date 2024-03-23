import os
import requests
import re

def list_songs():
  print("platform, song, url")
  list_apple_music_songs()
  list_spotify_songs()

def list_apple_music_songs():
  unique_song_urls = set()

  artist_albums_url = 'https://music.apple.com/us/artist/happy-happy-song-machine/1715027740/see-all?section=full-albums'
  albums_page = requests.get(artist_albums_url)

  # Look for URLs like this:
  # https://music.apple.com/us/album/happy-birthday-crew/1736292255
  album_urls = re.findall(r'https\:\/\/music\.apple\.com\/us\/album\/[^"]+', albums_page.text)

  for url in album_urls:
    album_page = requests.get(url)
    # Look for URLs like this:
    # https://music.apple.com/us/song/happy-birthday-mother/1715094972
    song_urls = re.findall(r'https\:\/\/music\.apple\.com\/us\/song\/[^"]+', album_page.text)

    for url in song_urls:
      unique_song_urls.add(url)

  sorted_song_urls = sorted(unique_song_urls)
  for url in sorted_song_urls:
    song_name = url.split('/')[-2].replace('-', ' ').title()
    print(f"apple music, {song_name}, {url}")

def list_spotify_songs():
  # Getting started docs:
  # https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app
  # 
  # I registered this app:
  # https://developer.spotify.com/dashboard/92ab56cdd37e4092b1ac031eae3efabc

  client_id = '92ab56cdd37e4092b1ac031eae3efabc'
  # Get secret from environment variable
  client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

  # Use the client ID and secret to get an access token
  token_url = 'https://accounts.spotify.com/api/token'
  token_params = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret 
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  token_response = requests.post(token_url, data=token_params, headers=headers)
  token = token_response.json()['access_token']

  headers = {
    'Authorization': f'Bearer {token}'
  }

  # Get all album IDs
  album_ids = []
  url = 'https://api.spotify.com/v1/artists/6E9qceaxgzpMz5ecZfni6O/albums?limit=50'
  while True:
    albums = requests.get(url, headers=headers)
    for album in albums.json()['items']:
      album_ids.append(album['id'])

    if albums.json()['next']:
      url = albums.json()['next']
    else:
      break

  # For each album, get a list of tracks
  for album_id in album_ids:
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50'
    while True:
      tracks = requests.get(url, headers=headers)
      for track in tracks.json()['items']:
        song_name = track['name']
        song_url = track['external_urls']['spotify']
        print(f"spotify, \"{song_name}\", {song_url}")
      
      if tracks.json()['next']:
        url = tracks.json()['next']
      else:
        break

if __name__ == "__main__":
  list_songs()
