from prefect import flow, task
from aws_terraform.train import Trainer
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import joblib
import tempfile


@task(retries=3, retry_delay_seconds=5)
def download_data():
    load_dotenv()
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    OBJECT_NAME = os.getenv("OBJECT_NAME")
    FILE_NAME = os.getenv("FILE_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_NAME + FILE_NAME)
    pd.read_csv(obj["Body"], header=None).to_csv(
        FILE_NAME, index=False, sep=",", header=None
    )

    downloaded_file = Path(FILE_NAME)
    if downloaded_file.is_file():
        print("File downloaded successfully")
    else:
        raise Exception("File not downloaded")
    return s3


@task
def train_model():
    trainer = Trainer()
    trainer.get_data("mockdata1.csv")
    trainer.fit()


@task(retries=3, retry_delay_seconds=5)
def upload_model(s3):
    model = joblib.load("model.pkl")

    BUCKET_NAME = os.getenv("BUCKET_NAME")
    MODEL_OBJECT_NAME = os.getenv("MODEL_OBJECT_NAME")

    with tempfile.TemporaryFile() as fp:
        joblib.dump(model, fp)
        fp.seek(0)
        s3.put_object(
            Body=fp.read(), Bucket=BUCKET_NAME, Key=MODEL_OBJECT_NAME + "model.pkl"
        )
    print("Model uploaded successfully")


@flow(log_prints=True)
def workflow():
    s3 = download_data()
    # usually there will be more tasks: data validation, preprocessing.
    train_model()
    upload_model(s3)


if __name__ == "__main__":
    workflow()
