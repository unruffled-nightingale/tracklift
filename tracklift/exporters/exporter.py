from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from tracklift.models.song import Song


class Exporter(ABC):
    @abstractmethod
    def tracks_in_playlist(self, playlist_id: str) -> List[str]:
        pass

    @abstractmethod
    def make_playlist(self, name: str, description: Optional[str]) -> Dict:
        pass

    @abstractmethod
    def add_song(self, existing_songs: List[str], playlist: Dict, song: Song) -> None:
        pass


class SongAlreadyExistsExporterException(Exception):
    ...


class UnknownExporterException(Exception):
    ...


class SongNotFoundExporterException(Exception):
    ...


class SpotifyUnreachableException(Exception):
    ...
