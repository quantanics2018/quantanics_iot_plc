from modbus import Modbus
import time, asyncio

### In config.toml file change slave = 1 and port = COMX (Check Device Manager for X)
### Baud Rate may shift randomly between 9600 and 19200 so change Baud = either in config.toml file
### Baud Rate = 19200

def button_event_listener(modbus:Modbus):
    while True:
        print("Reading : ", end ='')
        try:
            value:float = modbus.read_modbus(0)
            print(value, 'mA | ',end = '')
            value:float = modbus.read_modbus(1)
            print(value, 'mA')
        except Exception as e:
            print('Exception :', e)
        time.sleep(60)


async def initialize():
    modbus = Modbus()
    time.sleep(5) # wait for 5 sec to initialize all the modules
    results = await asyncio.gather(button_event_listener(modbus))

if __name__ == '__main__':
    asyncio.run(initialize())
