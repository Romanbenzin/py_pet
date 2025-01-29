import os
import pytest

from core.api_client import ApiClient
from urls import STELLAR


@pytest.fixture
def base_api():
    base_address = os.getenv("API_BASE_URL", STELLAR)
    return ApiClient(base_address=base_address)
