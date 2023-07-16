import pandas as pd
from mlflow_config import configure_mlflow
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow


class Experiment:
    def __init__(self, train_path, valid_path, run_id=None) -> None:
        self.train_path = train_path
        self.valid_path = valid_path
        self.run_id = run_id

    def read_dataframe(self, filename):
        df = pd.read_parquet(filename)

        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

        df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
        df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

        df = df[(df.duration >= 1) & (df.duration <= 60)]

        categorical = ["PULocationID", "DOLocationID"]
        df[categorical] = df[categorical].astype(str)

        return df

    def prepare_data(self):
        df_train, df_valid = self.read_dataframe("train.parquet"), self.read_dataframe(
            "valid.parquet"
        )
        df_train["PU_DO"] = df_train["PULocationID"] + "_" + df_train["DOLocationID"]
        df_valid["PU_DO"] = df_valid["PULocationID"] + "_" + df_valid["DOLocationID"]
        categorical = ["PU_DO"]
        numerical = ["trip_distance"]
        target = "duration"

        dv = DictVectorizer()

        train_dicts = df_train[categorical + numerical].to_dict(orient="records")
        valid_dicts = df_valid[categorical + numerical].to_dict(orient="records")

        X_train = dv.fit_transform(train_dicts)
        X_valid = dv.transform(valid_dicts)
        y_train = df_train[target].values
        y_valid = df_valid[target].values

        return X_train, y_train, X_valid, y_valid, dv

    def train_model(self, model, log_artifact=False):
        X_train, y_train, X_valid, y_valid, _ = self.prepare_data()

        configure_mlflow()
        with mlflow.start_run(run_id=self.run_id):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_valid)
            rmse = mean_squared_error(y_valid, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)
            if log_artifact:
                mlflow.sklearn.log_model(model, "model")
            
            self.cur_run_id = mlflow.active_run().info.run_id


        print(f"RMSE: {rmse}")
        

        return model
    
    def get_run_id(self):
        return self.cur_run_id


if __name__ == "__main__":
    exp = Experiment("train.parquet", "valid.parquet")
    ml = LinearRegression()
    exp.train_model(ml, log_artifact=False)
    print(exp.get_run_id())
