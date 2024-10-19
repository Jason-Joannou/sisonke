from typing import Dict, Optional

import requests

# LOCAT TESTING
BASE_URL = "http://127.0.0.1:5000"


def query_endpoint(endpoint_suffix: str, payload: Optional[Dict] = None) -> str:

    full_url = f"{BASE_URL}{endpoint_suffix}"
    print(full_url)

    try:
        if payload is not None:  # POST request
            response = requests.post(full_url, json=payload, timeout=5)
        else:  # GET request
            response = requests.get(full_url, timeout=5)

        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {full_url} - Payload: {payload}")
        return "Something went wrong, please try sending the action again."
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err} - URL: {full_url} - Payload: {payload}")
        return "Something went wrong, please try sending the action again."
    except Exception as err:
        print(f"Other error occurred: {err} - URL: {full_url} - Payload: {payload}")
        return "Something went wrong, please try sending the action again."
