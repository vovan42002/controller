import http.client
import settings
import json
import urllib.parse


def get_controller_id(email: str):
    connection = http.client.HTTPConnection(
        settings.CONTROLLER_API_HOST, port=settings.CONTROLLER_API_PORT
    )
    connection.request(
        "GET", "/controller/email?" + urllib.parse.urlencode({"email": email})
    )
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None
    controller = json.loads(response.read().decode())
    connection.close()
    return controller["id"]


def get_controller_info(id: int):
    connection = http.client.HTTPConnection(
        settings.CONTROLLER_API_HOST, port=settings.CONTROLLER_API_PORT
    )
    connection.request("GET", f"/controller/?id={id}")
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None

    controller = json.loads(response.read().decode())
    connection.close()
    return controller


def get_sensors(controller_id: int):
    connection = http.client.HTTPConnection(
        settings.CONTROLLER_API_HOST, port=settings.CONTROLLER_API_PORT
    )
    connection.request("GET", f"/controller/sensors?id={controller_id}")
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None

    sensors = json.loads(response.read().decode())
    connection.close()
    return sensors


def update_sensor(sensor_id: int, value: int):
    connection = http.client.HTTPConnection(
        settings.CONTROLLER_API_HOST, port=settings.CONTROLLER_API_PORT
    )
    body = {"actual": value}
    connection.request(
        "PATCH", f"/controller/sensor?id={sensor_id}", body=json.dumps(body)
    )
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None
    print("Sensor value updated successfully")
    connection.close()


def update_sensors(
    controller_id: int,
    temperature_air: int,
    temperature_soil: int,
    humidity_air: int,
    humidity_soil: int,
):
    sensors = get_sensors(controller_id=controller_id)
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
