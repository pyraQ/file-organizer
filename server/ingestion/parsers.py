from pathlib import Path
from typing import Dict, Optional
import json


class ParseError(Exception):
    """Raised when a file cannot be parsed."""


def detect_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ""}:
        return "text/plain"
    if suffix in {".json"}:
        return "application/json"
    if suffix in {".md"}:
        return "text/markdown"
    return "application/octet-stream"


def parse_file(path: Path) -> Dict[str, str]:
    """Parse a file into structured metadata."""
    mime = detect_mime(path)
    content = path.read_text(encoding="utf-8", errors="ignore")

    if mime == "application/json":
        try:
            loaded = json.loads(content)
            normalized = json.dumps(loaded, sort_keys=True)
        except json.JSONDecodeError as exc:
            raise ParseError(f"Failed to parse JSON: {path}") from exc
        return {"mime": mime, "content": normalized}

    return {"mime": mime, "content": content}


def summarize_content(content: str, limit: int = 240) -> str:
    return content[:limit] + ("..." if len(content) > limit else "")


def extract_metadata(path: Path) -> Dict[str, Optional[str]]:
    parsed = parse_file(path)
    return {
        "name": path.name,
        "mime": parsed.get("mime"),
        "summary": summarize_content(parsed.get("content", "")),
    }
