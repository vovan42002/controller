import http.client
import settings
import json


def get_sensor_values():
    connection = http.client.HTTPConnection(
        settings.ESPF_API_HOST, port=settings.ESPF_API_PORT
    )
    connection.request("GET", "/sensors")
    response = connection.getresponse()

    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None
    json_obj = json.loads(response.read().decode())
    connection.close()
    return json_obj


def enable_espf():
    connection = http.client.HTTPConnection(
        settings.ESPF_API_HOST, port=settings.ESPF_API_PORT
    )
    connection.request("GET", "/enable")
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None
    connection.close()
    return True


def disable_espf():
    connection = http.client.HTTPConnection(
        settings.ESPF_API_HOST, port=settings.ESPF_API_PORT
    )
    connection.request("GET", "/disable")
    response = connection.getresponse()
    if response.status != 200:
        print(f"Response code not 200. Code={response.status} Reason {response.reason}")
        return None
    connection.close()
    return True
