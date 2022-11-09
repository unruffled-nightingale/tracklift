from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup, Tag

from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist

from .importer import Importer


class Nts(Importer):
    def channel_url(self) -> str:
        return "https://www.nts.live/shows/"

    def tracklist_url(self) -> str:
        return "https://www.nts.live/shows"

    def get_playlist_songs(self, playlist_id: str) -> List[Song]:
        html = requests.get(f"{self.tracklist_url()}{playlist_id}")
        soup = BeautifulSoup(html.text, "html.parser")
        tracks = soup.find_all("li", {"class": "track"})
        return [
            Song(
                **{
                    "artist": t.find("span", {"class": "track__artist"}).text,
                    "title": t.find("span", {"class": "track__title"}).text,
                }
            )
            for t in tracks
        ]

    def get_tracklists(self, channel_id: str) -> List[Tracklist]:
        html = requests.get(f"{self.channel_url()}{channel_id}")
        tracklist_elements = [
            {
                "header_content": e.find("a", {"class": "nts-grid-v2-item__header"}),
                "footer_content": e.find("div", {"class": "nts-grid-v2-item__footer"}),
            }
            for e in BeautifulSoup(html.text, "html.parser")
            .find("div", {"class": "nts-grid-v2"})
            .find_all("div", {"class": "nts-grid-v2-item__content"})
        ]
        return [
            Tracklist(
                **{
                    "id": e["header_content"]["href"].replace("/shows/", ""),
                    "released": self._get_release_date(
                        e["header_content"].findNext("span").text
                    ),
                    "title": self._get_title(e["header_content"]),
                    "desc": self._get_desc(e),
                }
            )
            for e in tracklist_elements
        ]

    def _get_release_date(self, date_string: str) -> Optional[datetime]:
        if date_string is None or date_string == "":
            return None
        return datetime.strptime(date_string, "%d.%m.%y")

    def _get_title(self, element: Tag) -> Optional[str]:
        try:
            return element.find(
                "div", {"class": "nts-grid-v2-item__header__title"}
            ).text.strip()
        except AttributeError:
            return None

    def _get_desc(self, element: Tag) -> Optional[str]:
        try:
            location = element["header_content"].find_all("span")[1].text
            genres = ", ".join(
                [e.text for e in element["footer_content"].find_all("a")]
            )
            return f"{genres} recorded in {location}"
        except IndexError:
            return None
