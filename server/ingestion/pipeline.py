from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from server.core.config import get_settings
from server.db.metadb import MetaDB
from server.db.vectordb import VectorDB
from server.ingestion import parsers
from server.ingestion.hashing import hash_file
from server.ingestion.file_ops import copy_into_storage, ensure_storage_dir
from server.workflows.langgraph import LangGraphWorkflow, WorkflowResult


@dataclass
class IngestionJob:
    id: str
    source: Path
    status: str = "queued"
    metadata: Dict[str, str] = field(default_factory=dict)
    vector_id: Optional[str] = None


class IngestionPipeline:
    def __init__(self, storage_dir: Path, metadb: MetaDB, vectordb: VectorDB):
        self.storage_dir = storage_dir
        self.metadb = metadb
        self.vectordb = vectordb
        self.workflow = LangGraphWorkflow()
        self.queue: List[IngestionJob] = []
        ensure_storage_dir(self.storage_dir)

    def enqueue(self, path: Path) -> IngestionJob:
        job = IngestionJob(id=str(len(self.queue) + 1), source=path)
        self.queue.append(job)
        return job

    def process_next(self) -> Optional[IngestionJob]:
        if not self.queue:
            return None
        job = self.queue.pop(0)
        job.status = "processing"
        stored_path = copy_into_storage(job.source, self.storage_dir)
        job.metadata = parsers.extract_metadata(stored_path)
        job.metadata["hash"] = hash_file(stored_path) or ""

        workflow_result: WorkflowResult = self.workflow.run(stored_path, job.metadata)
        job.vector_id = self.vectordb.upsert(job.id, workflow_result.embedding)
        self.metadb.add_record(job.id, stored_path, workflow_result)
        job.status = "completed"
        return job

    def process_all(self) -> List[IngestionJob]:
        processed = []
        while self.queue:
            job = self.process_next()
            if job:
                processed.append(job)
        return processed

    def summary(self) -> List[Dict[str, str]]:
        return [
            {"id": job.id, "status": job.status, "path": str(job.source)}
            for job in self.queue
        ]


def create_default_pipeline() -> IngestionPipeline:
    settings = get_settings()
    metadb = MetaDB()
    vectordb = VectorDB(dimensions=settings.vector_dimensions)
    return IngestionPipeline(Path(settings.storage_dir), metadb, vectordb)
