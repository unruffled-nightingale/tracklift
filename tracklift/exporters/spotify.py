from typing import Dict, List, Optional

from spotipy import Spotify as SpotifyClient
from spotipy.oauth2 import SpotifyOAuth

from tracklift.env import env_get
from tracklift.exporters.exporter import (
    Exporter,
    SongAlreadyExistsExporterException,
    SongNotFoundExporterException,
    UnknownExporterException,
)
from tracklift.models.song import Song


class Spotify(Exporter):
    def __init__(self) -> None:
        self.sp = self.client()

    def client(self) -> SpotifyClient:
        scopes = ["playlist-modify-public"]
        auth = SpotifyOAuth(
            client_id=env_get("SPOTIFY_CLIENT_ID"),
            client_secret=env_get("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=env_get("SPOTIFY_REDIRECT_URL"),
            scope=scopes,
        )
        return SpotifyClient(auth_manager=auth)

    def playlists(self) -> List[Dict]:
        return [
            e for e in self.sp.user_playlists(self.sp.current_user()["id"])["items"]
        ]

    def create_playlist(self, name: str, description: Optional[str] = None) -> Dict:
        description = str(description or "")
        self.sp.user_playlist_create(
            self.sp.current_user()["id"], name, True, False, description
        )
        return self.get_playlist(name)

    def get_playlist(self, playlist_name: str) -> Dict:
        return [e for e in self.playlists() if e["name"] == playlist_name][0]

    def tracks_in_playlist(self, playlist_id: str) -> List[str]:
        self.sp.playlist_items(playlist_id)
        return [e["track"]["uri"] for e in self.sp.playlist_items(playlist_id)["items"]]

    def make_playlist(self, name: str, description: Optional[str] = None) -> Dict:
        if name not in [e["name"] for e in self.playlists()]:
            return self.create_playlist(name, description)
        else:
            return self.get_playlist(name)

    def add_song(self, existing_songs: List[str], playlist: Dict, song: Song) -> None:
        query = f"{song.title} | {song.artist}"
        try:
            results = self.sp.search(q=query, limit=1)
            track_id = results["tracks"]["items"][0]["uri"]
            if track_id in existing_songs:
                raise SongAlreadyExistsExporterException
            self.sp.playlist_add_items(playlist["id"], [track_id])
            existing_songs.append(track_id)
        except SongAlreadyExistsExporterException:
            raise SongAlreadyExistsExporterException(
                f"Song already exists in playlist for query {query!r}"
            )
        except IndexError:
            raise SongNotFoundExporterException(f"No song found for query {query!r}")
        except Exception as e:
            raise UnknownExporterException(
                f"Unknown exception when adding song for query {query!r} - {type(e)} - {e}"
            )
