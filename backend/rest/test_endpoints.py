import re
from fastapi.testclient import TestClient
from pathlib import Path

from ..main import app

test_files_dir = Path(__file__).parent.parent / "tests" / "assets"

client = TestClient(app)


def test_research():
    data = {
        "request": (
            "Using my notes on computational neuroscience, explain how memorization and "
            "generalization differ and how the classical hippocampus-to-neocortex account "
            "of memory consolidation relates to them. Then find recent research on the "
            "teacher-student-notebook model of memory and say whether it supports or "
            "challenges the classical account. Finish with a short answer to the question "
            "in my notes about a layer of fixed rule weights that backpropagation does "
            "not change, and point to any existing work on that idea."
        )
    }

    response = client.post("/api/research", json=data)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")

    lines = list(response.iter_lines())
    expected_message = f"Research request: {data['request']}"
    expected_lines = expected_message.splitlines()

    assert lines == expected_lines


def test_sources():
    files = [
        (
            "files",
            ("file1.md", open(test_files_dir / "file1.md", "rb"), "text/markdown"),
        ),
        (
            "files",
            ("file2.md", open(test_files_dir / "file2.md", "rb"), "text/markdown"),
        ),
    ]

    response = client.post("/api/sources", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")

    lines = list(response.iter_lines())
    expected_message = f"Added {len(files)} files"
    expected_lines = expected_message.splitlines()

    assert lines == expected_lines
