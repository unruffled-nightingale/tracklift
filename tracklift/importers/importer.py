from abc import ABC, abstractmethod
from typing import List, Tuple

from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist


class Importer(ABC):
    @abstractmethod
    def tracklist_url(self) -> str:
        raise NotImplementedError("This method cannot be called on the base class")

    @abstractmethod
    def channel_url(self) -> str:
        raise NotImplementedError("This method cannot be called on the base class")

    def get_songs(
        self, playlists: List[Tracklist]
    ) -> List[Tuple[Tracklist, List[Song]]]:
        return [(e, self.get_playlist_songs(e.id)) for e in playlists]

    @abstractmethod
    def get_playlist_songs(self, playlist_id: str) -> List[Song]:
        raise NotImplementedError("This method cannot be called on the base class")

    @abstractmethod
    def get_tracklists(self, channel_id: str) -> List[Tracklist]:
        raise NotImplementedError("This method cannot be called on the base class")
