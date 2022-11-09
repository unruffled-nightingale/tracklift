from typing import Dict, Type

from tracklift.importers.bbc import BbcSounds
from tracklift.importers.importer import Importer
from tracklift.importers.nts import Nts

IMPORTERS: Dict[str, Type[Importer]] = {"BBC Sounds": BbcSounds, "NTS": Nts}
