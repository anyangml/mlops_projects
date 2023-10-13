import pytest
import numpy as np


@pytest.fixture
def X():
    return np.random.rand(5000, 3)


@pytest.fixture
def y():
    return np.random.rand(5000)
