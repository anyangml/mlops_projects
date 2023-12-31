from pydantic import BaseModel
from pydantic import Field
from typing import List
from pydantic import validator
import numpy as np
from sklearn.model_selection import train_test_split


class Data(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True
        arbitrary_types_allowed = True

    _nfeature: int = 3
    _nsamples: int = 5000

    X: np.ndarray = Field(..., description="Input features")
    y: np.ndarray = Field(..., description="Outputs")

    @validator("X")
    def validate_X(cls, value):
        if value.shape != (cls._nsamples, cls._nfeature):
            raise ValueError(
                f"X must have {cls._nfeature} features and {cls._nsamples} samples."
            )
        return value

    @validator("y")
    def validate_y(cls, value):
        if value.shape != (cls._nsamples,):
            raise ValueError(f"y must have {cls._nsamples} samples.")
        return value

    def split_data(self, test_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=test_size
        )
        return X_train, X_test, y_train, y_test


class DataGenerator(BaseModel):
    class Config:
        extra = "forbid"
        frozen = True

    _features: List[str] = ["feature1", "feature2", "feature3"]
    _nfeature: int = 3
    _nsamples: int = 5000

    name: str
    intercepts: List[float] = Field(
        ...,
        description="Intercepts of the model to generate training data, 3 values are need.",
    )
    bias: float = Field(
        ..., description="Bias of the model to generate training data, 1 value is need."
    )

    @validator("intercepts")
    def validate_intercepts(cls, value):
        if len(value) != cls._nfeature:
            raise ValueError(f"Intercepts must have {cls._nfeature} values.")
        return value

    def generate_data(self):
        X = np.random.rand(self._nsamples, self._nfeature) * 10
        y = (
            np.dot(X, np.array(self.intercepts))
            + self.bias
            + np.random.normal(0, 1, self._nsamples)
        )
        return Data(X=X, y=y)

    def to_csv(self):
        data = self.generate_data()
        data = np.concatenate((data.X, data.y.reshape(-1, 1)), axis=1)
        np.savetxt(f"{self.name}.csv", data, delimiter=",")
