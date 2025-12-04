from pathlib import Path
from fastapi import APIRouter, HTTPException

from server.core.config import get_settings
from server.ingestion.pipeline import IngestionPipeline, create_default_pipeline
from server.schemas import (
    ConfigResponse,
    HealthResponse,
    IngestionRequest,
    IngestionResponse,
    QueueResponse,
    QueueItem,
    SearchRequest,
    SearchResponse,
    SearchHit,
)


router = APIRouter()
pipeline: IngestionPipeline = create_default_pipeline()


@router.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/config", response_model=ConfigResponse)
def config() -> ConfigResponse:
    settings = get_settings()
    return ConfigResponse(
        app_name=settings.app_name,
        version=settings.version,
        environment=settings.environment,
        storage_dir=settings.storage_dir,
        supported_parsers=settings.supported_parsers,
    )


@router.post("/ingest/files", response_model=IngestionResponse)
def ingest_file(payload: IngestionRequest) -> IngestionResponse:
    path = Path(payload.path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {payload.path}")
    job = pipeline.enqueue(path)
    pipeline.process_next()
    return IngestionResponse(job_id=job.id, status=job.status)


@router.get("/queue", response_model=QueueResponse)
def queue() -> QueueResponse:
    items = [QueueItem(**entry) for entry in pipeline.summary()]
    return QueueResponse(queue=items)


@router.post("/search", response_model=SearchResponse)
def search(payload: SearchRequest) -> SearchResponse:
    # Use vector similarity against stored embeddings
    query_embedding = pipeline.vectordb.generate_embedding(payload.query)
    scored = pipeline.vectordb.search(query_embedding, limit=payload.limit)
    hits = []
    for job_id, score in scored:
        record = next((record for record in pipeline.metadb.records if record.job_id == job_id), None)
        if record:
            hits.append(SearchHit(job_id=job_id, score=score, metadata=record.metadata))
    return SearchResponse(results=hits)
