from typing import Generator
import pytest
from fastapi.testclient import TestClient
import warnings

from soils.main import app

warnings.simplefilter(action="ignore", category=FutureWarning)


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
