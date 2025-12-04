from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from server.db.vectordb import VectorDB
from server.ingestion import parsers


@dataclass
class WorkflowResult:
    metadata: Dict[str, str]
    embedding: List[float]


class LangGraphWorkflow:
    def __init__(self):
        self.vectordb = VectorDB()

    def run(self, path: Path, metadata: Dict[str, str]) -> WorkflowResult:
        parsed = parsers.parse_file(path)
        metadata = {**metadata, **parsed}
        embedding = self.vectordb.generate_embedding(parsed.get("content", ""))
        return WorkflowResult(metadata=metadata, embedding=embedding)
