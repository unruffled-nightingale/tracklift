from typing import ContextManager, Optional

from alive_progress import alive_bar

from tracklift.trackers.tracker import Tracker


class CliTracker(Tracker):
    def progress_tracker(self, total: Optional[int] = None) -> ContextManager:
        return alive_bar(total, bar="smooth", spinner="notes2")

    def spinner(self) -> ContextManager:
        return alive_bar(
            None,
            bar=None,
            spinner="notes2",
            spinner_length=100,
            elapsed=False,
            monitor=False,
            stats=False,
        )
