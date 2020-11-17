import requests
import json
url = "http://127.0.0.1:5000/"

response = requests.get(url+"vsm/roadster_is_the_best")
print(response.json())
print("\n***Response Received!***\n")