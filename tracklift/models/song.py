from sqlalchemy import Column, String

from tracklift.models.base import Base


class Song(Base):
    __tablename__ = "songs"

    title = Column(String(200), primary_key=True)
    artist = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.title}   |   {self.artist}"
