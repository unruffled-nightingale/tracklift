from contextlib import ContextDecorator
from typing import ContextManager, Optional

from tracklift.trackers.tracker import Tracker


class SimpleTracker(Tracker):
    def progress_tracker(self, total: Optional[int] = None) -> ContextManager:
        return self._null_progress_tracker()

    def spinner(self) -> ContextManager:
        return self._null_progress_tracker()

    class _null_progress_tracker(ContextDecorator):
        def __enter__(self) -> ContextManager:
            return self

        def __exit__(self, *exc) -> bool:  # type: ignore
            return False

        def __call__(self, **kwargs) -> None:  # type: ignore
            pass
