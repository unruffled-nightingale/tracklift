import pytest

from tests.unit.conftest import requires_login
from tracklift.exporters.spotify import Spotify


@pytest.fixture
def exporter():
    return Spotify()


@requires_login
def test_playlists(exporter):
    assert len(exporter.playlists()) > 0


@requires_login
def test_create_playlist(exporter):
    exporter.create_playlist("test")


@requires_login
def test_get_playlist(exporter):
    assert "name" in exporter.get_playlist("test")


@requires_login
def test_tracks_in_playlist(exporter):
    tracks = exporter.tracks_in_playlist("spotify:playlist:5Ws5C20DpmwRntaA6Wvx7G")
    assert {t[0:14] for t in tracks} == {"spotify:track:"}


@requires_login
def test_make_playlist(exporter):
    exporter.make_playlist("test")
