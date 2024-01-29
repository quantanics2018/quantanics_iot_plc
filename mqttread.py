import json
import paho.mqtt.client as mqtt
from events import EventCallback
from configuration import Configuration, MqttCallbackConfiguration

class Mqt2():
    __mqtt_instance:mqtt = None
    __configs:dict = None

    def on_connect(client, userdata, flags, rc):
        print("MQTT Connected")
        client.subscribe('Data')

    def on_message(client, userdata, message):
        
        from Rad import menu

        payload = json.loads(message.payload.decode("utf-8"))
        menu(payload)

    def on_disconnect(client, userdata, rc):
        print("MQTT Disconnected")
        Mqt2.retry()

    def __new__(cls) -> None:
        if not hasattr(cls, 'instance'):
            Mqt2.__configs = Configuration().get_configs('Mqtt')
            Mqt2.connect_to_server()
            
            if Mqt2.__mqtt_instance != None:
                cls.instance = super(Mqt2, cls).__new__(cls)
        return cls.instance
    
    def connect_to_server():
        Mqt2.__mqtt_instance = mqtt.Client()
        Mqt2.__mqtt_instance.on_connect = Mqt2.on_connect
        Mqt2.__mqtt_instance.on_disconnect = Mqt2.on_disconnect
        Mqt2.__mqtt_instance.username_pw_set(Mqt2.__configs["username"], Mqt2.__configs["password"])
        Mqt2.add_callbacks()
        try:
            Mqt2.__mqtt_instance.connect_async(Mqt2.__configs["host"],Mqt2.__configs["port"])
            Mqt2.__mqtt_instance.loop_start()
            Mqt2.__mqtt_instance.on_message = Mqt2.on_message
        except Exception as e:
            raise Exception(e)
        
    @staticmethod
    def retry() -> None:
        Mqt2.connect_to_server()

    @staticmethod
    def disconnect() -> None:
        Mqt2.__mqtt_instance.disconnect()

    @staticmethod
    def connection_status() -> bool:
        return Mqt2.__mqtt_instance.is_connected()
    
    @staticmethod
    def add_callbacks():
        print("adding callbacks")
        Mqt2.__mqtt_instance.message_callback_add(Mqt2.__configs["config_update_topic"],MqttCallbackConfiguration.on_message)
        Mqt2.__mqtt_instance.message_callback_add(Mqt2.__configs["events_topic"], EventCallback.on_message)
        Mqt2.__mqtt_instance.on_message = Mqt2.on_message
    
    @staticmethod
    def send(payload:dict, topic:str):
        Mqt2.__mqtt_instance.publish(topic,json.dumps(payload),Mqt2.__configs["qos"])
