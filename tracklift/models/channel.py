from sqlalchemy import Column, String

from tracklift.models.base import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(String(10), primary_key=True)

    def __repr__(self) -> str:
        return f"Channels(id={self.id!r})"
