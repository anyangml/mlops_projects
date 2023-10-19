import joblib
import numpy as np


model = joblib.load("model.pkl")


def predict_handler(event, context):
    """
    Parameter:
    -----------
    event: JSON
        The data to be predicted. {'feature': [1,2,3]}
    Returns:
    --------
    prediction: JSON
        The prediction of the model.

    """
    # Here, we load the model from the docker container
    # Alternatively, we can load the model from S3 by providing credentials
    model = joblib.load("model.pkl")

    features = np.array(event["feature"]).reshape(1, -1)
    prediction = model.predict(features)
    return {"prediction": prediction.tolist(), "coefficient": model.coef_.tolist(), "intercept": model.intercept_.tolist}

