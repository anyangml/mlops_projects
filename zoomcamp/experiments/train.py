import pandas as pd
from mlflow_config import configure_mlflow
from sklearn.feature_extraction import DictVectorizer 

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

    dv = DictVectorizer()

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    valid_dicts = df_valid[categorical + numerical].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)
    X_valid = dv.transform(valid_dicts)

    return X_train, X_valid, dv

if __name__ == '__main__':
    df_train = read_dataframe('train.parquet')
    df_valid = read_dataframe('valid.parquet')
    X_train, X_valid, _ = prepare_data(df_train, df_valid)
    print(X_train)