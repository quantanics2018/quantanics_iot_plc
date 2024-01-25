from modbus import Modbus
import time, asyncio

### In config.toml file change slave = 3 and port = COMX (Check Device Manager for X)
### Baud Rate may shift randomly between 9600 and 19200 so change Baud = either in config.toml file
### Baud Rate = 9600

def button_event_listener(modbus:Modbus):

    while True:

        val = int(input('Enter register to toggle : '))
        value:float = modbus.read_modbusbit(val)
        print(value)
        modbus.write_modbus(val,not value)

def clear_all(modbus):

    try:
        for i in range(0,14):
            modbus.write_modbus(i,0)
    except Exception as e:
        print('Exception :', e)

def run_all(modbus):

    try:
        for i in range(0,14):
            modbus.write_modbus(i,1)
    except Exception as e:
        print('Exception :', e)

async def initialize():
    modbus = Modbus()
    time.sleep(5) # wait for 5 sec to initialize all the modules
    clear_all(modbus=modbus)
    time.sleep(3)
    run_all(modbus)
    time.sleep(3)
    clear_all(modbus)
    results = await asyncio.gather(button_event_listener(modbus))

if __name__ == '__main__':
    asyncio.run(initialize())
