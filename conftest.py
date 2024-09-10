import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

assignment_dir = Path(__file__).parents[1].absolute()


sys.path.insert(0, str(assignment_dir))


@pytest.fixture
def client():
    """Fixture to return an HTTP client that can talk to our test app"""
    from app import app

    return TestClient(app)
