import settings
import schedule
import time
from controller import get_controller_info, update_sensors, get_controller_id
from espf import disable_espf, enable_espf, get_sensor_values
from scheduler import is_enable
from temp_settings import TempSettings


def runner():
    if TempSettings.first_run is True:
        print("First")
        controller_id = get_controller_id(email=settings.EMAIL)
        print(f"Controller id: {controller_id}")
        if controller_id is None:
            return
        print(f"Controller id: {controller_id}")
        TempSettings.controller_id = controller_id
        print("Start extractiong data controller info")
        controller_info = get_controller_info(id=controller_id)
        print(controller_info)
        if controller_info is None:
            return
        TempSettings.last_changed = controller_info["last_changed"]
        TempSettings.first_run = False
    print("running")
    controller_info = get_controller_info(id=TempSettings.controller_id)
    print("Controller info")
    print(controller_info)
    # if TempSettings.last_changed != controller_info["last_changed"]:
    print("Go to switcher")
    TempSettings.last_changed = controller_info["last_changed"]
    swither(controller_info=controller_info)
    print("changed")
    sensors(TempSettings.controller_id)


def sensors(controller_id: int):
    print("In function sensors")
    sensor_values = get_sensor_values()
    print("Sensor values")
    print(sensor_values)
    if sensor_values is None:
        return
    temperature_air = int(sensor_values["temperature_air"])
    temperature_soil = int(sensor_values["temperature_soil"])
    humidity_air = int(sensor_values["humidity_air"])
    humidity_soil = int(sensor_values["humidity_soil"])
    update_sensors(
        controller_id=controller_id,
        temperature_air=temperature_air,
        temperature_soil=temperature_soil,
        humidity_air=humidity_air,
        humidity_soil=humidity_soil,
    )


def swither(controller_info):
    print("In switcher")
    force_enable = controller_info["force_enable"]
    status = controller_info["status"]
    if force_enable:
        print("Force enable")
        enable_espf()
    else:
        if status:
            print("Enabled")
            enable_espf()
        else:
            print("Disable")
            disable_espf()

        start_time = controller_info["start_time"]
        end_time = controller_info["end_time"]
        print(f"Start time:{ start_time}")
        print(f"End time: {end_time}")

        if start_time != -1 and end_time != -1:
            if is_enable(
                start_time=start_time,
                end_time=end_time,
            ):
                print("Enable espf")
                enable_espf()
            else:
                print("Disable espf")
                disable_espf()


schedule.every(settings.TIMEOUT).seconds.do(runner)

while True:
    schedule.run_pending()
    time.sleep(1)
