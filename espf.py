import http.client
import settings
import json
import requests

URL = settings.ESPF_URL


def get_sensor_values():
    try:
        response = requests.get(URL + "/sensors")
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def enable_espf():
    try:
        response = requests.get(URL + "/enable")
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def disable_espf():
    try:
        response = requests.get(URL + "/disable")
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")
