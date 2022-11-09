import json
from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from tracklift.importers.importer import Importer
from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist


class BbcSounds(Importer):
    def channel_url(self) -> str:
        return "https://www.bbc.co.uk/sounds/brand/"

    def tracklist_url(self) -> str:
        return "https://www.bbc.co.uk/sounds/play/"

    def get_playlist_songs(self, playlist_id: str) -> List[Song]:
        html = requests.get(f"{self.tracklist_url()}{playlist_id}")
        soup = BeautifulSoup(html.text, "html.parser")
        scripts = soup.find_all("script")
        data = scripts[18].text.replace(" window.__PRELOADED_STATE__ = ", "")[0:-2]
        tracklist = list(
            filter(
                lambda e: e["title"] == "Tracklist", json.loads(data)["modules"]["data"]
            )
        )
        return [
            Song(
                **{"artist": e["titles"]["primary"], "title": e["titles"]["secondary"]}
            )
            for e in tracklist[0]["data"]
        ]

    def get_tracklists(self, channel_id: str) -> List[Tracklist]:
        html = requests.get(f"{self.channel_url()}{channel_id}")
        soup = BeautifulSoup(html.text, "html.parser")
        scripts = soup.find_all("script")
        string_data = scripts[18].text.replace(" window.__PRELOADED_STATE__ = ", "")[
            0:-2
        ]
        tracklists = json.loads(string_data)["modules"]["data"][1]["data"]
        return [
            Tracklist(
                **{
                    "id": e["urn"].split(":")[-1],
                    "released": self._get_release_date(e["release"]["date"]),
                    "title": f"{e['titles']['primary']} - {e['titles']['secondary']}",
                    "desc": [
                        e[1] for e in sorted(e["synopses"].items()) if e[1] is not None
                    ][0],
                }
            )
            for e in tracklists
        ]

    def _get_release_date(self, date_string: Optional[str]) -> Optional[datetime]:
        if date_string is None:
            return None
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
