from datetime import datetime

import pytest

from tracklift.importers import Nts
from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist


@pytest.fixture
def importer():
    return Nts()


def test_get_playlist_songs(importer):
    songs = importer.get_playlist_songs(
        "/the-large/episodes/the-large-7th-october-2022"
    )
    assert len(songs) > 0
    assert {type(p) for p in songs} == {Song}


def test_get_tracklists(importer):
    playlists = importer.get_tracklists("the-large")
    assert len(playlists) > 0
    assert {type(p) for p in playlists} == {Tracklist}


def test_get_release_date(importer):
    assert type(importer._get_release_date("21.10.20")) == datetime
