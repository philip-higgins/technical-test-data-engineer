import requests
from datetime import datetime
import json
import random
import os

BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = ["/tracks", "/users", "/listen_history"]


def fetch_data(endpoint, base_url):
    url = f"{base_url}{endpoint}"
    try:
        # Generate a random number of entries for each category/endpoint
        response = requests.get(url, params={"size": random.randint(1, 100)})
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def daily_data_retrieval(base_url):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    success = True  # Track if all endpoints were successful

    # Fetch data for each endpoint
    for endpoint in ENDPOINTS:
        data = fetch_data(endpoint, base_url)

        if data is None:
            success = False
            continue  # Skip saving and go to the next endpoint

        # Save data to a JSON file in the data folder
        try:
            filename = f"../../data/{endpoint.strip('/')}_{timestamp}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)  # Ensure directory exists
            with open(filename, "w") as f:
                json.dump(data, f)
            print(f"Data saved to {filename}")

        except FileNotFoundError:
            print("Error: The specified file path does not exist.")
            success = False

        except PermissionError:
            print("Error: Insufficient permissions to write to the file.")
            success = False

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            success = False

    return 'SUCCESS' if success else 'PARTIAL_SUCCESS_OR_ERROR'


daily_data_retrieval(BASE_URL)
