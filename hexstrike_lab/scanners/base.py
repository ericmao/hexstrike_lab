from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Scanner(ABC):
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    @abstractmethod
    def run(self, target_host: str) -> dict[str, Any]:
        """Return a single finding dict matching schema $defs/finding."""
