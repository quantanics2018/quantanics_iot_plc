import json
import time
from configuration import Configuration
from modbus import Modbus

class EventCallback:
    def on_message(client, userdata, msg):
        value = json.loads(msg.payload)
        if value['status'] == "Inactive" or value['status'] == "Machine OFF":
            LEDNotification.notify("led2")

class LEDNotification:
    __led_configs = None
    __modbus_instance = None
    
    @staticmethod
    def initialize():
        LEDNotification.__led_configs = Configuration().get_configs('LED_Modbus')
        LEDNotification.__modbus_instance = Modbus()

    @staticmethod
    def notify(led_no):
        value = LEDNotification.__led_configs[led_no]
        LEDNotification.__modbus_instance.write_modbus(0,value)
    
    @staticmethod
    def notify_blink(led_no):
        value = LEDNotification.__led_configs[led_no]
        for i in range(0,2):
            LEDNotification.__modbus_instance.write_modbus(0,value)
            time.sleep(0.5)
            LEDNotification.__modbus_instance.write_modbus(0,0)
