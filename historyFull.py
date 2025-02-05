import requests
import json

API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'

url = "https://fr24api.flightradar24.com/api/historic/flight-positions/full"
params = {
  'bounds': '50.682,46.218,14.422,22.243',
  'timestamp': '1702383145'
}

headers = {
  'Accept': 'application/json',
  'Accept-Version': 'v1',
  'Authorization': f'Bearer {API_TOKEN}'
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
