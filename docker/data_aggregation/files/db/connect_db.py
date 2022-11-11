from typing import Optional

import mariadb
#from mariadb import Connection

from config import DB_CFG, SYS_PREFS

DB_HOST = DB_CFG['DB_HOST']
DB_NAME = DB_CFG['DB_NAME']
DB_USER = DB_CFG['DB_USER']
DB_PW = DB_CFG['DB_PW']
DB_PORT = DB_CFG['DB_PORT']

TIMEZONE=SYS_PREFS['TIMEZONE']

TABLE_NAME_MEAS = "ble_meas"
TABLE_NAME_STATIONS = "ble_stations"
TABLE_NAME_TIMEWINDOWS = "ble_timewindows"


def connect_db(): # -> Optional[Connection]:
    print("Connect DB '{}'".format(DB_NAME))
    db_conn = mariadb.connect(
        user=DB_USER,
        password=DB_PW,
        host=DB_HOST,
        port=DB_PORT
    )
    print("- done")

    init_db(db_conn)

    db_conn = mariadb.connect(
        user=DB_USER,
        password=DB_PW,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    init_tables(db_conn)

    db_conn.auto_reconnect = True

    return db_conn

def init_db(db_conn)->None:
    print("Init DB...")
    cursor = db_conn.cursor()

    sql_tz="SET GLOBAL time_zone = '{}';".format(TIMEZONE)
    cursor.execute(sql_tz)

    sql_create_db="""
    CREATE DATABASE IF NOT EXISTS {};
    """.format(DB_NAME)
    cursor.execute(sql_create_db)
    db_conn.commit()
    cursor.close()
    print("- done")


def init_tables(db_conn) -> None:
    print("Init tables...")
    cursor = db_conn.cursor()

    sql_create_station_table="""
    CREATE TABLE IF NOT EXISTS {} (
        id VARCHAR(100) PRIMARY KEY UNIQUE,
        name TEXT,
        lat DOUBLE,
        lon DOUBLE,
        latest_status TEXT,
        fw_version TEXT
        )
    """.format(TABLE_NAME_STATIONS)
    cursor.execute(sql_create_station_table)

    sql_create_timewindow_table="""
    CREATE TABLE IF NOT EXISTS {} (
        time_from DATETIME PRIMARY KEY UNIQUE,
        time_to DATETIME,
        size INTEGER
        )
    """.format(TABLE_NAME_TIMEWINDOWS)
    cursor.execute(sql_create_timewindow_table)

    sql_create_meas_table="""
    CREATE TABLE IF NOT EXISTS {} (
        mac VARCHAR(64) NOT NULL,
        time_in DATETIME NOT NULL,
        time_out DATETIME NOT NULL,
        manuf TEXT,
        is_cwa BOOLEAN,
        name TEXT,
        public_addr BOOLEAN,
        station VARCHAR(100) NOT NULL,
        timewindow DATETIME NOT NULL,
        
        PRIMARY KEY (mac, station, timewindow),
        FOREIGN KEY (station) REFERENCES {} (id),
        FOREIGN KEY (timewindow) REFERENCES {} (time_from)
    )
    """.format(TABLE_NAME_MEAS, TABLE_NAME_STATIONS, TABLE_NAME_TIMEWINDOWS)

    cursor.execute(sql_create_meas_table)
    db_conn.commit()
    cursor.close()
    print("- done")
