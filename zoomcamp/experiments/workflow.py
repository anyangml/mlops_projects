from prefect import flow, task
from env import DATA_URL_TRAIN, DATA_URL_VALID
from train import Experiment
from sklearn.linear_model import LinearRegression
import requests

@task(retries=3, retry_delay_seconds=5)
def download_data(url, file_name):
    file_path = f"data/{file_name}"
    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Error: {response.status_code}")

@task
def train_model():
    experiment = Experiment("data/train.parquet", "data/valid.parquet")
    ml = LinearRegression()
    experiment.train_model(ml, log_artifact=False)


@flow
def workflow():
    download_data(DATA_URL_TRAIN, "train.parquet")
    download_data(DATA_URL_VALID, "valid.parquet")
    train_model()

if __name__ == "__main__":
    workflow()