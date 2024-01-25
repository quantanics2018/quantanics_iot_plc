from modbus import Modbus
import time, asyncio

### In config.toml file change slave = 2 and port = COMX (Check Device Manager for X)
### Baud Rate may shift randomly between 9600 and 19200 so change Baud = either in config.toml file
### Baud Rate = 19200

def button_event_listener(modbus:Modbus):
    while True:
        print("Reading : ", end ='')
        try:
            value:float = modbus.read_modbus(0)
            print(value, 'V | ',end = '')
            value:float = modbus.read_modbus(1)
            print(value, 'V')
        except Exception as e:
            print('Exception :', e)
        time.sleep(0.5)


async def initialize():
    modbus = Modbus()
    modbus.connect_device()
    time.sleep(5) # wait for 5 sec to initialize all the modules
    results = await asyncio.gather(button_event_listener(modbus))

if __name__ == '__main__':
    asyncio.run(initialize())
