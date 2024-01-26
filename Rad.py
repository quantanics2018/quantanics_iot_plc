from modbus import Modbus
import time, asyncio, logging, minimalmodbus, serial, pytimedinput
from sql import SQL
from mqtt import Mqtt
from datetime import datetime

def menu(current,voltage,relay,sql:SQL):

    while True:

        choice, timed = pytimedinput.timedInput("",5)

        if timed:

            begin(current,voltage,relay,sql,20)

        else:

            if choice == '1':

                execute_relay(relay,1)

            elif choice == '0':

                execute_relay(relay,0)

            elif choice == '9':

                register_address = int(input("Enter address to toggle : "))
                dat = relay.read_modbusbit(register_address)
                relay.write_modbus(choice,not dat)

            else:

                print('Unknown Sequence.')
                print(choice)

def begin(current,voltage,relay,sql:SQL,count):

    ### Time between each connection
    ### 10ms keeps disconnecting every other time
    ### 15ms works but has a high possibility of errors
    ### 25ms running for quite some time did not produce any errors
    device_minimum_access_time = 0.1
    iteration_count = 0

    for i in range(count):

        try:

            time.sleep(device_minimum_access_time)
            current.configs['baudrate'] = 19200
            current.configs['slave'] = 1
            current.connect_device()
            current1, current2 = readCurrent(current,iteration_count)
            time.sleep(device_minimum_access_time)
            voltage.configs['baudrate'] = 19200
            voltage.configs['slave'] = 2
            voltage.connect_device()
            voltage1, voltage2 = readVoltage(voltage,iteration_count)
            time.sleep(device_minimum_access_time)
            relay.configs['baudrate'] = 9600
            relay.configs['slave'] = 3
            relay.connect_device()
            relay_values = readRelay(relay,iteration_count)
            print()
            sql.push(current1,current2,voltage1,voltage2,relay_values)
            '''mqtt.send({
                "current1" : current1,
                "current2" : current2,
                "voltage1" : voltage1,
                "voltage2" : voltage2,
                "relay_values" : relay_values,
                "gateway_time":str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            },'data_log')'''
            iteration_count += 1

        except serial.serialutil.SerialException as e:

            print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus.')
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.warning("Port Error. Most likely Modbus unplugged or device drivers not alllowing serial communication. Error message :  " + str(e))
            time.sleep(2)

        except Exception as e:

            print('Unknown Error : ', e)
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.critical("Not Expected Error. Error message : " + str(e))
            time.sleep(2)         

    return

def readCurrent(modbus:Modbus, iteration_count):

    message = f'[{iteration_count}] '
    message += "Current : "
    current1 = modbus.read_modbus(0)
    current2 = modbus.read_modbus(1)

    if current1 + current2 < 10:

        message += "0 mA"

    elif current1 + current2 > 40500:

        message += "0 mA"

    else:

        message += str(current1) + "mA | " + str(current2) + "mA"

    print(message)
    return current1, current2

def readVoltage(modbus:Modbus, iteration_count):

    message = f'[{iteration_count}] '
    message += "Voltage : "
    voltage1 = modbus.read_modbus(0)
    voltage2 = modbus.read_modbus(1)

    if voltage1 + voltage2 < 25:

        message += "0 V"

    elif voltage1 + voltage2 > 20200:

        message += "0 V"

    else:

        message += str(voltage1) + " V | " + str(voltage2) + " V"

    print(message)
    return voltage1, voltage2

def readRelay(modbus:Modbus, iteration_count):

    relay_values = [modbus.read_modbusbit(val) for val in range(0,14)]
    relay_values_str = list(map(str,relay_values))
    message= f'[{iteration_count}]' + " | " + ' | '.join(relay_values_str) + " |"
    print(message)
    return relay_values_str

def execute_relay(modbus,n):

    for i in range(0,14):
        modbus.write_modbus(i,n)

async def initialize():

    try:

        current = Modbus()
        current.configs['baudrate'] = 19200
        current.configs['slave'] = 1
        current.connect_device()
        time.sleep(1)
        voltage = Modbus()
        voltage.configs['baudrate'] = 19200
        voltage.configs['slave'] = 2
        voltage.connect_device()
        time.sleep(1)
        relay = Modbus()
        relay.configs['baudrate'] = 9600
        relay.configs['slave'] = 3
        relay.connect_device()
        time.sleep(1)
        sql = SQL()
        time.sleep(3)
        print("Ready")
        results = await asyncio.gather(menu(current,voltage,relay,sql))

    except serial.serialutil.SerialException as e:

        print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus.')
        file_handler = logging.FileHandler('example.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.error("Port Error. Most likely Modbus unplugged or device drivers not alllowing serial communication. Error message :  " + str(e))
        time.sleep(2)

if __name__ == '__main__':
    asyncio.run(initialize())