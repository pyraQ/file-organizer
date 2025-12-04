from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from server.workflows.langgraph import WorkflowResult


@dataclass
class MetaRecord:
    job_id: str
    path: Path
    metadata: Dict[str, str]


class MetaDB:
    def __init__(self):
        self.records: List[MetaRecord] = []

    def add_record(self, job_id: str, path: Path, result: WorkflowResult) -> MetaRecord:
        record = MetaRecord(job_id=job_id, path=path, metadata=result.metadata)
        self.records.append(record)
        return record

    def search(self, query: str) -> List[MetaRecord]:
        lowered = query.lower()
        return [
            record
            for record in self.records
            if lowered in record.metadata.get("summary", "").lower()
            or lowered in record.metadata.get("name", "").lower()
        ]
