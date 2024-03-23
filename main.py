import requests
import re

def list_songs():
  print("platform, song, url")
  list_apple_music_songs()
  # list_spotify_songs()

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

# def list_spotify_songs():
#   print("spotify, song1, https://open.spotify.com/track/0y4TKcc7p2H6P0GJlt01EI")
#   print("spotify, song2, https://open.spotify.com/track/0y4TKcc7p2H6P0GJlt01EI")
#   print("spotify, song3, https://open.spotify.com/track/0y4TKcc7p2H6P0GJlt01EI")

if __name__ == "__main__":
  list_songs()