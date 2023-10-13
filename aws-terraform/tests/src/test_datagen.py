import pytest
from src.datagen import Data, DataGenerator
import numpy as np


def test_data_validation():
    with pytest.raises(ValueError, match="y must have"):
        Data(X=np.array([[1, 2, 3]]), y=np.array([1, 2, 3, 4]))


def test_data_split(X, y):
    data = Data(X=X, y=y)

    X_train, y_train, X_test, y_test = data.split_data(test_size=0.2)

    assert len(X_train) == 4000
    assert len(X_test) == 1000
    assert len(y_train) == 4000
    assert len(y_test) == 1000


def test_data_generator():
    generator = DataGenerator(name="test", intercepts=[1, 2, 3], bias=0.5)
    data = generator.generate_data()

    assert len(data.X) == 5000
    assert len(data.y) == 5000


def test_data_generator_validation():
    with pytest.raises(ValueError):
        DataGenerator(name="test", intercepts=[1, 2], bias=0.5)
