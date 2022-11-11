from config import MQTT_CFG
from db.store_meas import store_latest_station_status
from util import mqtt as mqtt_kd, ble_parse
import json

from container_classes.time_window import TimeWindow
from container_classes.time_windows import TimeWindows
from util.ble_parse import get_json_value

time_windows: TimeWindows = TimeWindows()

SENSORS_TOPIC = MQTT_CFG['SENSORS_TOPIC']
ADMIN_TOPIC = MQTT_CFG['ADMIN_TOPIC']


def on_sensor_message(client, userdata, msg) -> None:
    station_id = msg.topic
    json_obj = msg.payload.decode('utf-8')
    try:
        data: json = json.loads(json_obj)
    except Exception as ex:
        print("- could not parse json", ex)
        return
    data["station"] = station_id

    # Add to datastructure and db
    timestamp: int = ble_parse.get_timestamp_from_data(data)
    cur_tw: TimeWindow = time_windows.get_cur_timewindow(timestamp)
    ble_parse.add_new_meas(cur_tw, data)

    # print(time_windows.to_string(indent=2))


def on_admin_message(client, userdata, msg) -> None:
    # replace 'admin' by 'sensor'
    station_id = 'sensor' + msg.topic.replace(msg.topic[:5], '')

    json_obj = msg.payload.decode('utf-8')
    try:
        data: json = json.loads(json_obj)
    except Exception as ex:
        # should happen on every not status message ;)
        print("- could not parse json:", json_obj, ex)
        return

    # TODO: Update fw only if there is a value in json
    # TODO: Add latest update info timestamp
    station_status = get_json_value(data, 'status', 'unknown')
    fw_version = get_json_value(data, 'firmware', 'unknown')
    store_latest_station_status(station_id, station_status, fw_version)


def main() -> None:
    mqtt_client = mqtt_kd.init()

    # mqtt_client.on_message = on_message
    mqtt_client.message_callback_add(SENSORS_TOPIC, on_sensor_message)
    mqtt_client.message_callback_add(ADMIN_TOPIC, on_admin_message)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqtt_client.loop_forever()
    # mqtt_client.loop_start()


if __name__ == '__main__':
    main()
