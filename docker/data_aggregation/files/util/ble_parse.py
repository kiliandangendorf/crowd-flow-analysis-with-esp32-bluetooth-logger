import json
import hashlib
import datetime as dt

from config import BLE_CFG

from container_classes.time_window import TimeWindow
from manuf_lookup.manuf_lookup import get_manuf_from_data
from util.time import timestamp_to_tz_aware


def is_cwa(data: json) -> bool:
    # corona is UUID "fd6f" (no manufacturer, eg. 0000fd6f-0000-1000-8000-00805f9b34fb)
    service_uuid: str = get_json_value(data, 'serviceUUID')
    if not service_uuid:
        return False
    significant = service_uuid[4:8]
    if significant.lower() == "fd6f":
        return True
    return False


def get_timestamp_from_data(data: json, default_ts: int = 0) -> int:
    return int(get_json_value(data, 'timestamp', default_ts))


def add_new_meas(tw_meas: TimeWindow, data: json):
    timestamp: int = int(get_json_value(data, 'timestamp', 0))
    time: dt.datetime = timestamp_to_tz_aware(timestamp)
    if time < tw_meas.time_from:
        print("too low", time, tw_meas.time_from)
        return
    time = time+dt.timedelta(microseconds=int(get_json_value(data, 'micros', 0)))

    station_id: str = get_json_value(data, 'station')

    mac = get_json_value(data, 'address', "")
    if BLE_CFG['PRIVACY_HASH']:
        mac: str = hashlib.sha256(mac.encode("utf-8")).hexdigest()
    # TODO: Check MAC for blacklist (TBD)

    # already in list
    if tw_meas.station_contains_meas(station_id, mac, time):
        # we don't need more work, if we've done below already
        return

    public_addr: bool = int(get_json_value(data, 'addrType', 1)) == 0

    # else create new meas
    manuf_data: str = get_json_value(data, 'manufData', "")
    service_uuid: str = get_json_value(data, 'serviceUUID')
    clear_mac: str = get_json_value(data, 'address', "")
    manufacturer: str = get_manuf_from_data(public_addr, clear_mac, manuf_data, service_uuid)

    cwa: bool = is_cwa(data)

    name: str = get_json_value(data, 'name', "")
    if BLE_CFG['PRIVACY_HASH'] and not name.strip():
        # only hash name if not empty
        name: str = hashlib.sha256(name.encode("utf-8")).hexdigest()

    tw_meas.add_meas(station_id, mac, time, manufacturer, cwa, name, public_addr)
    # print(tw_meas.to_string(2))

    # get_json_value(data,'appearance',""),
    ## get_json_value(data,'serviceUUID',""),

    # print done
    # print("-received info: "+json.dumps(data))


def get_json_value(data, key, default=None) -> str:
    if key in data:
        return data[key]
    else:
        return default
