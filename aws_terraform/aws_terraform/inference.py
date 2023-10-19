from flask import Flask, jsonify, request
import joblib
import json
import numpy as np

app = Flask(__name__)

model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    """
    Parameter:
    -----------
    data: JSON
        The data to be predicted. {'feature': [1,2,3]}
    Returns:
    --------
    prediction: JSON
        The prediction of the model.
    
    """
    data = json.loads(request.data)
    
    features = np.array(data['feature']).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
