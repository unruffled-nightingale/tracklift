from abc import ABC, abstractmethod
from typing import ContextManager, List, Optional

from tracklift.models.song import Song


class Tracker(ABC):
    def __init__(self) -> None:
        self.succeeded: List[Song] = []
        self.errored: List[Song] = []
        self.already_exists: List[Song] = []
        self.not_found: List[Song] = []

    @abstractmethod
    def progress_tracker(self, total: Optional[int] = None) -> ContextManager:
        ...

    @abstractmethod
    def spinner(self) -> ContextManager:
        ...
