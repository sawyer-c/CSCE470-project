import requests
import json
url = "http://127.0.0.1:5000/"

response = requests.get(url+"vsm/ford_mustang")
print(response.json())