import os

import pytest


@pytest.fixture
def fixture_data_dir():
    return os.path.join(os.path.dirname(__file__), 'data')
