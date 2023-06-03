import settings
import schedule
import time
from controller import (
    get_controller_info,
    get_sensors,
    update_sensors,
    get_controller_id,
)
from espf import disable_espf, enable_espf, get_sensor_values
from utils import is_enable, convert_unix_to_HHMMSS
from temp_settings import TempSettings

TAG_DAILY = "daily_tasks"


def runner():
    if TempSettings.first_run is True:
        controller_id = get_controller_id(email=settings.EMAIL)
        if controller_id is None:
            print(f"Can't extract controller with id: {controller_id}")
            return
        TempSettings.controller_id = controller_id
        controller_info = get_controller_info(id=controller_id)
        if controller_info is None:
            print(f"Can't extract controller info. Controller id: {controller_id}")
            return
        TempSettings.last_changed = controller_info["last_changed"]
        TempSettings.first_run = False
    controller_info = get_controller_info(id=TempSettings.controller_id)
    print(f"Controller info: {controller_info}")
    if TempSettings.last_changed != controller_info["last_changed"]:
        TempSettings.last_changed = controller_info["last_changed"]
        swither(controller_info=controller_info)
    sensors(TempSettings.controller_id)
    enable_by_expectations(TempSettings.controller_id)


def sensors(controller_id: int):
    sensor_values = get_sensor_values()
    if sensor_values is None:
        print(f"Can't extract sensor values for controller wit id {controller_id}")
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
    force_enable = controller_info["force_enable"]
    status = controller_info["status"]
    if force_enable:
        print("Force enable")
        enable_espf()
    else:
        if status:
            print("Enabled by status")
            enable_espf()
        else:
            print("Disabled by status")
            disable_espf()

        start_time = controller_info["start_time"]
        end_time = controller_info["end_time"]
        repeat = controller_info["repeat"]

        if start_time != -1 and end_time != -1:
            if repeat:
                schedule_every_day(
                    start_time_unix=start_time, end_time_unix=end_time, enabled=True
                )
            else:
                schedule_every_day(
                    start_time_unix=start_time, end_time_unix=end_time, enabled=False
                )

            if is_enable(
                start_time=start_time,
                end_time=end_time,
            ):
                print("Enable espf")
                enable_espf()
            else:
                print("Disable espf")
                disable_espf()


def enable_by_expectations(controller_id: int):
    sensors_in_db = get_sensors(controller_id=controller_id)
    if sensors_in_db is None:
        return None
    for sensor in sensors_in_db:
        sensor_actual = sensor["Sensor"]["actual"]
        sensor_expected = sensor["Sensor"]["expected"]
        if sensor_actual >= sensor_expected:
            disable_espf()
        else:
            enable_espf()


def schedule_every_day(start_time_unix: int, end_time_unix: int, enabled: bool):
    if enabled:
        schedule_start_time = convert_unix_to_HHMMSS(time_unix=start_time_unix)
        schedule_end_time = convert_unix_to_HHMMSS(time_unix=end_time_unix)
        schedule.every().day.at(schedule_start_time).do(enable_espf).tag(TAG_DAILY)
        schedule.every().day.at(schedule_end_time).do(enable_espf).tag(TAG_DAILY)
        print(f"Schedule start at: {schedule_start_time}, end at: {schedule_end_time}")
    else:
        schedule.clear(TAG_DAILY)
        print("Canceled daily jobs")


schedule.every(settings.TIMEOUT).seconds.do(runner)

while True:
    schedule.run_pending()
    time.sleep(1)
