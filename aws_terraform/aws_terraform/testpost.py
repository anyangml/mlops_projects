import requests

url = "http://127.0.0.1:8000/predict"

response = requests.post(url, data='{"feature":[1,2,3]}')

print(response.text)
