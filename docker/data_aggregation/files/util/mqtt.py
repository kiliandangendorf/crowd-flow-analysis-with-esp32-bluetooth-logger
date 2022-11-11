import paho.mqtt.client as mqtt
import ssl

from config import MQTT_CFG

SECURE_MQTT=MQTT_CFG['SECURE_MQTT']

MQTT_BROKER=MQTT_CFG['MQTT_BROKER']
MQTT_CLIENT_ID=MQTT_CFG['MQTT_CLIENT_ID']
MQTT_USERNAME=MQTT_CFG['MQTT_USERNAME']
MQTT_PASSWD=MQTT_CFG['MQTT_PASSWD']
SENSORS_TOPIC=MQTT_CFG['SENSORS_TOPIC']
ADMIN_TOPIC=MQTT_CFG['ADMIN_TOPIC']

ABS_CA_PATH=MQTT_CFG['ABS_CA_PATH']

if SECURE_MQTT:
    MQTT_PORT=8883
else:
    MQTT_PORT=1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #Subscribing in on_connect() means that if we lose the connection and
    #reconnect then subscriptions will be renewed.
    client.subscribe(SENSORS_TOPIC)
    client.subscribe(ADMIN_TOPIC)

def init()->mqtt.Client:
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False)
    client.on_connect = on_connect
    client.username_pw_set(username=MQTT_USERNAME,password=MQTT_PASSWD)

    if SECURE_MQTT:
        # TLS context
        sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # Load the CA certificates used for validating the peer's certificate
        sslSettings.load_verify_locations(cafile=ABS_CA_PATH,capath=None,cadata=None);
        # Load client cert
        client.tls_set_context(sslSettings)
    
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    return client