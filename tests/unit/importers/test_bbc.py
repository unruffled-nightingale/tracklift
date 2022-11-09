from datetime import datetime

import pytest

from tracklift.importers.bbc import BbcSounds
from tracklift.models.song import Song
from tracklift.models.tracklist import Tracklist


@pytest.fixture
def importer():
    return BbcSounds()


def test_get_playlist_songs(importer):
    songs = importer.get_playlist_songs("m001cyw6")
    assert len(songs) > 0
    assert {type(p) for p in songs} == {Song}


def test_get_tracklists(importer):
    playlists = importer.get_tracklists("m0008w2m")
    assert len(playlists) > 0
    assert {type(p) for p in playlists} == {Tracklist}


def test_get_release_date(importer):
    assert type(importer._get_release_date("2020-10-13T00:00:00Z")) == datetime
