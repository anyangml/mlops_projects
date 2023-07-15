import pandas as pd
from mlflow_config import configure_mlflow
from sklearn.feature_extraction import DictVectorizer 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow

def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    
    return df

def prepare_data(df_train, df_valid):
    df_train['PU_DO'] = df_train['PULocationID'] + '_' + df_train['DOLocationID']
    df_valid['PU_DO'] = df_valid['PULocationID'] + '_' + df_valid['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    target = 'duration'

    dv = DictVectorizer()

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    valid_dicts = df_valid[categorical + numerical].to_dict(orient='records')

    X_train = dv.fit_transform(train_dicts)
    X_valid = dv.transform(valid_dicts)
    y_train = df_train[target].values
    y_valid = df_valid[target].values

    return X_train, y_train, X_valid, y_valid, dv

def train_model(X_train, y_train, X_valid, y_valid):
    configure_mlflow()
    with mlflow.start_run():
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_valid)
        rmse = mean_squared_error(y_valid, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

    print(f"RMSE: {rmse}")
    # mlflow.log_artifact(model)

    return model

if __name__ == '__main__':
    df_train = read_dataframe('train.parquet')
    df_valid = read_dataframe('valid.parquet')
    X_train, y_train, X_valid, y_valid, _ = prepare_data(df_train, df_valid)
    train_model(X_train, y_train, X_valid, y_valid)