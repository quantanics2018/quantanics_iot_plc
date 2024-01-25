from modbus import Modbus
import time, asyncio, logging, minimalmodbus, serial

def begin():

    current = Modbus()
    voltage = Modbus()
    relay = Modbus()
    iteration_count = 0

    while True:

        ### Time between each connection
        ### 10ms keeps disconnecting every other time
        ### 15ms works but has a high possibility of errors
        ### 25ms running for quite some time did not produce any errors
        device_minimum_access_time = 0.025

        try:

            time.sleep(device_minimum_access_time)
            current.configs['baudrate'] = 19200
            current.configs['slave'] = 1
            current.connect_device()
            readCurrent(current,iteration_count)
            time.sleep(device_minimum_access_time)
            voltage.configs['baudrate'] = 19200
            voltage.configs['slave'] = 2
            voltage.connect_device()
            readVoltage(voltage,iteration_count)
            time.sleep(device_minimum_access_time)
            relay.configs['baudrate'] = 9600
            relay.configs['slave'] = 3
            relay.connect_device()
            readRelay(relay,iteration_count)
            print()
            iteration_count += 1

        except minimalmodbus.ModbusException as e:

            print('Unable to communicate with device. Please check the power subsystem and the wiring configuration')
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.warning("Modbus cannot be connected. Possible reasons are very low device_minimum_access_time (Unable to read multiple slave in very less time). Error message : " + str(e))
            time.sleep(2)

        except KeyboardInterrupt as e:

            writeRelay(relay)
            break

        except PermissionError as e:

            print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus. ', e)
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.warning("Port Error. Most likely Modbus unplugged or device drivers not alllowing serial communication. Error message :  " + str(e))
            time.sleep(2)

        except serial.serialutil.SerialException as e:

            print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus. ', e)
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

        message += str(current1) + "mA |" + str(current2) + "mA"

    print(message)

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

def readRelay(modbus:Modbus, iteration_count):

    relay_values = [modbus.read_modbusbit(val) for val in range(0,14)]
    relay_values_str = list(map(str,relay_values))
    message= f'[{iteration_count}]' + " | " + ' | '.join(relay_values_str) + " |"
    print(message)

def writeRelay(modbus:Modbus):

    while True:

        pattern_value = int(input("Enter Sequence : "))

        if pattern_value == 1:

            execute_relay(modbus,1)

        elif pattern_value == 0:

            execute_relay(modbus,0)

        elif pattern_value == 9:

            register_address = int(input("Enter address to toggle : "))
            dat = modbus.read_modbusbit(register_address)
            modbus.write_modbus(pattern_value,not dat)

        else:

            print('Unknown Sequence.')
            break

def execute_relay(modbus,n):

    for i in range(0,14):
        modbus.write_modbus(i,n)

async def initialize():

    try:

        time.sleep(3)
        results = await asyncio.gather(begin())

    except serial.serialutil.SerialException as e:

        print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus.')
        file_handler = logging.FileHandler('example.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.error("Port Error. Most likely Modbus unplugged or device drivers not alllowing serial communication. Error message :  " + str(e))
        time.sleep(2)

if __name__ == '__main__':
    asyncio.run(initialize())