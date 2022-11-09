import time

import pytest

from tracklift.trackers.cli_tracker import CliTracker
from tracklift.trackers.simple_tracker import SimpleTracker

TRACKERS = [CliTracker(), SimpleTracker()]


@pytest.mark.parametrize("tracker", TRACKERS)
def test_progress_tracker(tracker):
    try:
        with tracker.progress_tracker() as track:
            for i in range(0, 3):
                time.sleep(0.1)
                track()
    except Exception:
        pytest.fail(f"{tracker.__class__}.progress_bar raised as error")


@pytest.mark.parametrize("tracker", TRACKERS)
def test_spinner(tracker):
    try:
        with tracker.spinner():
            for i in range(0, 3):
                time.sleep(0.1)
    except Exception:
        pytest.fail(f"{tracker.__class__}.spinner raised as error")
