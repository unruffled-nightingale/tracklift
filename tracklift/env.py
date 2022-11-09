import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def env_get(key: str) -> Optional[str]:
    try:
        return os.environ[key]
    except KeyError:
        raise EnvNotFound(key)


class EnvNotFound(KeyError):
    ...
