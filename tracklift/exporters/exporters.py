from typing import Dict, Type

from tracklift.exporters.exporter import Exporter
from tracklift.exporters.spotify import Spotify

EXPORTERS: Dict[str, Type[Exporter]] = {
    "Spotify": Spotify,
}
