from typing import List

from container_classes.meas import BleMeas, Meas
from container_classes.station import Station
from container_classes.time_window import TimeWindow
from db.connect_db import connect_db, TABLE_NAME_MEAS, TABLE_NAME_STATIONS, TABLE_NAME_TIMEWINDOWS

db_conn = connect_db()


def store_timewindow(timewindow: TimeWindow):
    for station in timewindow.stations:
        for meas in station.meas:
            _store_meas(meas, station, timewindow)


def store_timewindows(timewindows: List[TimeWindow]):
    for timewindow in timewindows:
        store_timewindow(timewindow)


def _store_meas(meas: Meas, station: Station, timewindow: TimeWindow) -> bool:
    # Check if it's BleMeas, then cast
    if isinstance(meas, BleMeas):
        return _store_ble_meas(meas, station, timewindow)
    else:
        # TODO: do something with generic type ;)
        return False


def _store_ble_meas(meas: BleMeas, station: Station, timewindow: TimeWindow) -> bool:
    done = False
    cursor = db_conn.cursor()

    try:
        # Insert station if not exists
        # See: https://stackoverflow.com/a/4596409/11438489
        sql_update_station = """
        INSERT IGNORE INTO {} (id)
            VALUES (?) 
            ON DUPLICATE KEY UPDATE id=VALUES(id);
        """.format(TABLE_NAME_STATIONS)
        cursor.execute(sql_update_station, (
            station.id,
        ))

        # Insert or update timewindow
        # See: https://stackoverflow.com/a/22679523/11438489
        sql_update_timewindow = """
        INSERT INTO {} (time_from, time_to, size)
            VALUES (?, ?, ?) 
            ON DUPLICATE KEY UPDATE time_from=VALUES(time_from), time_to=VALUES(time_to), size=VALUES(size); 
        """.format(TABLE_NAME_TIMEWINDOWS)
        cursor.execute(sql_update_timewindow, (
            timewindow.time_from,
            timewindow.time_to,
            timewindow.window_size_in_minutes
        ))

        # Insert meas
        sql_insert_meas = """
        INSERT INTO {} (
            mac,
            time_in,
            time_out,
            manuf,
            is_cwa,
            name,
            public_addr,
            station,
            timewindow
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """.format(TABLE_NAME_MEAS)

        cursor.execute(sql_insert_meas, (
            meas.id,
            meas.time_in,
            meas.time_out,
            meas.manuf,
            meas.is_cwa,
            meas.name,
            meas.public_addr,
            station.id,
            timewindow.time_from
        ))
        db_conn.commit()

        done = True
    except Exception as ex:
        print("Error inserting data", ex)
        raise
    finally:
        cursor.close()
        return done


def store_latest_station_status(station_id: str, status: str, fw_version: str) -> bool:
    done = False
    cursor = db_conn.cursor()

    # TODO: only store fw_version if not None

    try:
        # Insert station if not exists
        # See: https://stackoverflow.com/a/4596409/11438489
        sql_update_station = """
        INSERT INTO {} (id, latest_status, fw_version)
            VALUES (?,?,?) 
            ON DUPLICATE KEY UPDATE latest_status=VALUES(latest_status), fw_version=VALUES(fw_version);
        """.format(TABLE_NAME_STATIONS)
        cursor.execute(sql_update_station, (
            station_id,
            status,
            fw_version
        ))
        db_conn.commit()

        done = True
    except Exception as ex:
        print("Error inserting data", ex)
        raise
    finally:
        cursor.close()
        return done
