import http.client
import settings
import json
import urllib.parse
import requests
import logging

URL = f"http://{settings.CONTROLLER_API_HOST}:{settings.CONTROLLER_API_PORT}"


def get_controller_id(email: str):
    try:
        response = requests.get(URL + "/controller/email", params={"email": email})

        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None

        response_json = response.json()
        if not response_json["id"]:
            return None

        return response_json["id"]
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def get_controller_info(id: int):
    try:
        response = requests.get(URL + "/controller/", params={"id": id})
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None

        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def get_sensors(controller_id: int):
    try:
        response = requests.get(
            URL + "/controller/sensors", params={"id": controller_id}
        )
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def update_sensor(sensor_id: int, value: int):
    try:
        response = requests.patch(
            URL + "/controller/sensor", params={"id": sensor_id}, json={"actual": value}
        )
        if response.status_code != 200:
            print(f"Response code not 200. Code={response.status_code}")
            return None
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(f"Http error {error}")
    except requests.exceptions.ConnectionError as conerr:
        print(f"Connection error {conerr}")


def update_sensors(
    controller_id: int,
    temperature_air: int,
    temperature_soil: int,
    humidity_air: int,
    humidity_soil: int,
):
    sensors = get_sensors(controller_id=controller_id)
    print(f"Sensors info: {sensors}")
    if sensors is None:
        return None
    for sensor in sensors:
        sensor_id = sensor["Sensor"]["id"]
        if sensor["Sensor"]["type"] == "temperature_air":
            update_sensor(sensor_id=sensor_id, value=temperature_air)
        elif sensor["Sensor"]["type"] == "temperature_soil":
            update_sensor(sensor_id=sensor_id, value=temperature_soil)
        elif sensor["Sensor"]["type"] == "humidity_air":
            update_sensor(sensor_id=sensor_id, value=humidity_air)
        elif sensor["Sensor"]["type"] == "humidity_soil":
            update_sensor(sensor_id=sensor_id, value=humidity_soil)
    return True
