import json
import paho.mqtt.client as mqtt
from events import EventCallback
from configuration import Configuration, MqttCallbackConfiguration

class Mqtt():
    __mqtt_instance:mqtt = None
    __configs:dict = None

    def on_connect(client, userdata, flags, rc):
        print("MQTT Connected")
        client.subscribe('Data')

    def on_disconnect(client, userdata, rc):
        print("MQTT Disconnected")
        Mqtt.retry()

    def __new__(cls) -> None:
        if not hasattr(cls, 'instance'):
            Mqtt.__configs = Configuration().get_configs('Mqtt')
            Mqtt.connect_to_server()
            
            if Mqtt.__mqtt_instance != None:
                cls.instance = super(Mqtt, cls).__new__(cls)
        return cls.instance
    
    def connect_to_server():
        Mqtt.__mqtt_instance = mqtt.Client()
        Mqtt.__mqtt_instance.on_connect = Mqtt.on_connect
        Mqtt.__mqtt_instance.on_disconnect = Mqtt.on_disconnect
        Mqtt.__mqtt_instance.username_pw_set(Mqtt.__configs["username"], Mqtt.__configs["password"])
        try:
            Mqtt.__mqtt_instance.connect_async(Mqtt.__configs["host"],Mqtt.__configs["port"])
            Mqtt.__mqtt_instance.loop_start()
        except Exception as e:
            raise Exception(e)
        
    @staticmethod
    def retry() -> None:
        Mqtt.connect_to_server()

    @staticmethod
    def disconnect() -> None:
        Mqtt.__mqtt_instance.disconnect()

    @staticmethod
    def connection_status() -> bool:
        return Mqtt.__mqtt_instance.is_connected()
    
    @staticmethod
    def send(payload:dict, topic:str):
        Mqtt.__mqtt_instance.publish(topic,json.dumps(payload),Mqtt.__configs["qos"])
