import requests
import json

# Define the JSON data
data = {'problem': 'binary_search'}

# Send a POST request to the URL
url = 'http://127.0.0.1:7432'
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    result = response.json()
    print('Response:', result)
else:
    print(f'Error: {response.status_code}, {response.text}')