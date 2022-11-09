from sqlalchemy import Column, Date, ForeignKey, String

from tracklift.models.base import Base


class Tracklist(Base):
    __tablename__ = "tracklists"

    id = Column(String(10), primary_key=True)
    title = Column(String(100), nullable=False)
    desc = Column(String(200), nullable=True)
    released = Column(Date, nullable=True)
    channel_id = Column(String, ForeignKey("channels.id"), nullable=False)

    def __repr__(self) -> str:
        return (
            f"{self.released.strftime('%Y-%m-%d') if self.released else 'xxxx-xx-xx'}  |  "
            f"{self.title}  | "
            f"{ (self.desc[:50] + '...') if len(self.desc) > 50 else self.desc}"
        )
