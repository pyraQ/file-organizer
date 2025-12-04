from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ConfigResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    storage_dir: str
    supported_parsers: List[str]


class IngestionRequest(BaseModel):
    path: Path = Field(..., description="Absolute path to the file to ingest")
    tags: Optional[List[str]] = None


class IngestionResponse(BaseModel):
    job_id: str
    status: str


class QueueItem(BaseModel):
    id: str
    status: str
    path: str


class QueueResponse(BaseModel):
    queue: List[QueueItem]


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


class SearchHit(BaseModel):
    job_id: str
    score: float
    metadata: Dict[str, str]


class SearchResponse(BaseModel):
    results: List[SearchHit]
