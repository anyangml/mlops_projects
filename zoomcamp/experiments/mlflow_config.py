MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
EXPERIMENT_NAME = "nyc-taxi-experiment"
ARTIFACT_REPOSITORY = "s3://anyang-mlops/zoomcamp/nyc-taxi-experiment"

import mlflow


def configure_mlflow():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    if mlflow.get_experiment_by_name(EXPERIMENT_NAME) is None:
        mlflow.create_experiment(
            name=EXPERIMENT_NAME, artifact_location=ARTIFACT_REPOSITORY
        )

    mlflow.set_experiment(EXPERIMENT_NAME)
