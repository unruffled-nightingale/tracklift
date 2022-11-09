import logging
from typing import List, Optional, Tuple

from tracklift.exporters.exporter import (
    Exporter,
    SongAlreadyExistsExporterException,
    SongNotFoundExporterException,
    UnknownExporterException,
)
from tracklift.exporters.exporters import EXPORTERS
from tracklift.importers import IMPORTERS
from tracklift.importers.importer import Importer
from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist
from tracklift.trackers.simple_tracker import SimpleTracker
from tracklift.trackers.tracker import Tracker

log = logging.getLogger(__name__)


class Tracklift:
    def __init__(self, platform: str, tracker: Optional[Tracker] = None):
        self.platform = platform
        self.importer = self._get_importer()
        self.exporter = self._get_exporter()
        self.tracker = tracker or SimpleTracker()

    def _get_importer(self) -> Importer:
        log.info(f"Retrieving {self.platform!r} importer...")
        return IMPORTERS[self.platform]()

    def _get_exporter(self) -> Exporter:
        log.info("Retrieving importer for Spotify")
        return EXPORTERS["Spotify"]()

    def get_playlists(self, channel_id: str) -> List[Tracklist]:
        with self.tracker.spinner():
            log.info(f"Retrieving from playlists {channel_id!r}...")
            playlists = self.importer.get_tracklists(channel_id)
            log.info(f"Retrieved {len(playlists)} playlists")
            return playlists

    def get_songs(
        self, playlists: List[Tracklist]
    ) -> List[Tuple[Tracklist, List[Song]]]:
        with self.tracker.spinner():
            log.info("Retrieving songs...")
            songs = self.importer.get_songs(playlists)
            log.info(f"Retrieved {len(songs)} songs")
            return songs

    def add_songs(self, all_songs: List[Tuple[Tracklist, List[Song]]]) -> None:
        log.info("Adding songs to playlist...")

        with self.tracker.progress_tracker(sum(len(e[1]) for e in all_songs)) as track:
            for tracklist, songs in all_songs:
                playlist_name = (
                    f"{tracklist.title} - {tracklist.released.strftime('%Y-%m-%d')}"
                )
                playlist = self.exporter.make_playlist(playlist_name, tracklist.desc)
                existing_songs = self.exporter.tracks_in_playlist(playlist["id"])
                for song in songs:
                    log.debug(f"Adding song {song.title} by {song.artist}...")
                    try:
                        self.exporter.add_song(existing_songs, playlist, song)
                        self.tracker.succeeded.append(song)
                    except SongAlreadyExistsExporterException:
                        self.tracker.already_exists.append(song)
                    except SongNotFoundExporterException:
                        self.tracker.not_found.append(song)
                    except UnknownExporterException:
                        self.tracker.errored.append(song)
                    track()
                    log.debug("Song added")
                log.info("Added songs to playlist")
