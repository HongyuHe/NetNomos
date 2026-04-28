from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


@dataclass(slots=True)
class ArtifactStore:
    root: Path

    @classmethod
    def create(cls, base: Path, dataset_name: str, grammar_name: str) -> "ArtifactStore":
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        root = base / f"{stamp}_{dataset_name}_{grammar_name}"
        root.mkdir(parents=True, exist_ok=False)
        return cls(root=root)

    def write_json(self, relative: str, data: Any) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, sort_keys=True, default=str))
        return path

    def write_jsonl(self, relative: str, rows: Iterable[dict[str, Any]]) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as handle:
            for row in rows:
                handle.write(json.dumps(row, default=str) + "\n")
        return path

    def write_text(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path
