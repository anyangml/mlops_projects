
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "nyc-taxi-experiment"
ARTIFACT_REPOSITORY = "s3://anyang-mlops/zoomcamp/nyc-taxi-experiment"

import mlflow

def configure_mlflow():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.create_experiment(EXPERIMENT_NAME,ARTIFACT_REPOSITORY)