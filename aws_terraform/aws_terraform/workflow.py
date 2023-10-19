from prefect import flow, task
from aws_terraform.train import Trainer
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd


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


@task
def train_model():
    trainer = Trainer()
    trainer.get_data("mockdata1.csv")
    trainer.fit()


@flow(log_prints=True)
def workflow():
    download_data()
    # usually there will be more tasks: data validation, preprocessing.
    train_model()


if __name__ == "__main__":
    workflow()
