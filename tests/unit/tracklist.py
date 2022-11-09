import pytest

from tracklift.main import Tracklift
from tracklift.models.song import Song

PARAMETERS = [
    ("BBC Sounds", "m0008w2m", "m001cyw6"),
    ("NTS", "the-large", "the-large-7th-october-2022"),
]


@pytest.mark.parametrize("platform, channel_id, tracklist_id", PARAMETERS)
def test_tracklift_without_adding_songs(platform, channel_id, tracklist_id):
    tl = Tracklift(platform)
    playlists = tl.get_playlists(channel_id)
    songs = tl.get_songs(playlists[0:1])
    assert len(songs) > 0
    assert {type(p) for p in songs} == {Song}


# @requires_login
@pytest.mark.parametrize("platform, channel_id, tracklist_id", PARAMETERS)
def test_tracklift(platform, channel_id, tracklist_id):
    tl = Tracklift(platform)
    playlists = tl.get_playlists(channel_id)
    songs = tl.get_songs(playlists[0:2])
    # reduce the size of the songs list to improve speed of test
    songs = [(e[0], e[1][0:3]) for e in songs]
    tl.add_songs(songs)
