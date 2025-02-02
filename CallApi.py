import requests

API_TOKEN = '9e09878e-71fc-41bd-b41f-2bf99149679c|DmVwjwtjTEq5rS2MPKJ0Y1XmtL7TyhqhDyIR9bSra1f7c38f'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/live/flight-positions/light'

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"

# Define the headers, including the Authorization header with your API token
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}

# Define any query parameters, if needed (optional)
params = {
    'bounds': '50.682,46.218,14.422,22.243'  # Slovenia IntAirport coordinates
}

# Make the GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print("Live Flight Positions:")
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
