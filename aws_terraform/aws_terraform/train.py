import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline

# from sklearn.preprocessing import StandardScaler
import joblib
from datagen import Data


class Trainer:
    def get_data(self, filename) -> None:
        data: np.ndarray = np.genfromtxt(filename, delimiter=",")
        self.raw_data: Data = Data(X=data[:, :-1], y=data[:, -1])

    def fit(self) -> None:
        X_train, X_test, y_train, y_test = self.raw_data.split_data()
        # self.pipeline = Pipeline([('scaler', StandardScaler()),
        #                           ("lasso", LinearRegression())])
        self.pipeline = Pipeline([("lasso", LinearRegression())])
        self.pipeline.fit(X_train, y_train)
        y_pred = self.pipeline.predict(X_test)
        print(
            f"Training Finished --> coef: {self.pipeline[0].coef_, self.pipeline[0].intercept_}, MSE: {mean_squared_error(y_test, y_pred)}"
        )
        joblib.dump(self.pipeline, "model.pkl")
