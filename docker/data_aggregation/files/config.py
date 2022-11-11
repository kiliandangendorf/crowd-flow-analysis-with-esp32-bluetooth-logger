SYS_PREFS={
    "TIMEZONE": "Europe/Berlin",
}

GENERAL_CFG={
    "FIRST_POSSIBLE_TS": 1600000000,
    "TIME_WINDOW_IN_MIN": 2,
    "MAX_TIME_WINDOW_IN_MEMORY": 30,
}

BLE_CFG={
    "PRIVACY_HASH": True,
}

MQTT_CFG={
    "SECURE_MQTT": True,
    "MQTT_BROKER": "Hostname or IP",
    "MQTT_CLIENT_ID": "data_aggregation",
    "MQTT_USERNAME": "reader_ble",
    "MQTT_PASSWD": "Password for reader_ble",
    "SENSORS_TOPIC": "sensor/BLE/Scanner/#",
    "ADMIN_TOPIC": "admin/BLE/Scanner/#",
    "ABS_CA_PATH": "certs/ca.crt",
}

DB_CFG={
    "DB_HOST": "mariadb",
    "DB_NAME": "ble_tracking_data",
    "DB_USER": "root",
    "DB_PW": "qwerty",
    "DB_PORT": 3306,
}
