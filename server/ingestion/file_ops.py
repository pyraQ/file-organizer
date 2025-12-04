from pathlib import Path
from typing import Optional


class FileNotFound(Exception):
    pass


def ensure_storage_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_into_storage(source: Path, storage_dir: Path) -> Path:
    if not source.exists():
        raise FileNotFound(f"Missing file: {source}")
    ensure_storage_dir(storage_dir)
    target = storage_dir / source.name
    target.write_bytes(source.read_bytes())
    return target


def read_partial(path: Path, limit: int = 1024) -> Optional[str]:
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8", errors="ignore")
    return content[:limit]
