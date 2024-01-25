import time
import asyncio
from modbus import Modbus
from mqtt import Mqtt
from datetime import datetime
from configuration import Configuration
from events import LEDNotification

def send_response_to_hardware():
    LEDNotification.notify_blink('led1')

def button_event_listener(configs:Configuration,mqtt:Mqtt, modbus:Modbus):
    while True:
        print("Reading...........")
        try:
            value:int = modbus.read_modbus(2)
            if value > 0 and value != "null" or None:
                mqtt.send({"button_id":value,
                           "gateway_time":str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                           "machine_id":configs.get_configs("Machine")["machine_id"]},
                           configs.get_configs("Mqtt")["button_inputs_topic"])
                modbus.write_modbus(4,1) # reset button system
                send_response_to_hardware() # blink response
        except Exception as e:
            mqtt.send({"Exception":str(e)},configs.get_configs("Mqtt")["exceptions_topic"]) 
        time.sleep(0.5)
       
async def initialize():
    mqtt = Mqtt()
    configuration = Configuration()
    modbus = Modbus()
    LEDNotification.initialize()
    time.sleep(5) # wait for 5 sec to initialize all the modules
    results = await asyncio.gather(button_event_listener(configuration,mqtt,modbus))

if __name__ == '__main__':
    asyncio.run(initialize())
