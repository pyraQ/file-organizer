from pathlib import Path

from server.ingestion.hashing import hash_content, hash_file
from server.ingestion.pipeline import create_default_pipeline


def test_hash_content_changes():
    assert hash_content("hello") != hash_content("world")


def test_hash_file(tmp_path: Path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("sample text")
    assert hash_file(test_file)


def test_pipeline_processes_file(tmp_path: Path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("content")

    pipeline = create_default_pipeline()
    job = pipeline.enqueue(test_file)
    processed = pipeline.process_next()

    assert processed is not None
    assert job.id == processed.id
    assert processed.status == "completed"
    assert processed.metadata.get("name") == "sample.txt"
