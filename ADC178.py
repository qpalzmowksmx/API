import requests
import json

url = "https://fr24api.flightradar24.com/api/flight-tracks"
params = {
  'flight_id': '35f2ffd9'
}
headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': 'Bearer <token>'
}

try:
  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  data = response.json()
  print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
  print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
