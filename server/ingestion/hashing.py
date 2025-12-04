from hashlib import sha256
from pathlib import Path
from typing import Optional


def hash_content(content: str) -> str:
    return sha256(content.encode("utf-8")).hexdigest()


def hash_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return hash_content(path.read_text(encoding="utf-8", errors="ignore"))
