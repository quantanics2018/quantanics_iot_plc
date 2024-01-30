import time
import asyncio
import logging
import serial
from mqtt import Mqtt
from datetime import datetime
from current import Current
from voltage import Voltage
from relay import Relay
from fourrelay import fourRelay
from mqttread import Mqt2

relay = Relay()
current = Current()
voltage = Voltage()
fourrelay = fourRelay()

async def begin(current, voltage, relay, mqtt):

    device_minimum_access_time = 0.02
    iteration_count = 0

    while True:

        try:

            with open('data.txt') as f:
                data = f.read()

            output = int(data)

            await asyncio.sleep(device_minimum_access_time)
            current.connect_device()
            current1, current2, current_relay = await readCurrent(current, iteration_count)

            await asyncio.sleep(device_minimum_access_time)
            voltage.connect_device()
            voltage1, voltage2, voltage_relay = await readVoltage(voltage, iteration_count)

            await read_volatage_current_relay(voltage_relay, current_relay, iteration_count)

            await asyncio.sleep(device_minimum_access_time)
            relay.connect_device()
            relay_values = await readRelay(relay, iteration_count)

            print()

            mqtt.send({
                "current": (current1 + current2) / 2,
                "voltage": (voltage1 + voltage2) / 2,
                "relay_values": relay_values,
                "gateway_time": str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            }, 'data_log')

            if output != -1:

                await execute(output)

            iteration_count += 1

            await asyncio.sleep(0)

        except serial.serialutil.SerialException as e:

            print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus.')
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.warning("Port Error. Most likely Modbus unplugged or device drivers not allowing serial communication. Error message :  " + str(e))
            time.sleep(2)

        except Exception as e:

            print('Unknown Error : ', e)
            file_handler = logging.FileHandler('example.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            logging.getLogger().addHandler(file_handler)
            logging.critical("Not Expected Error. Error message : " + str(e))
            time.sleep(2)

    return

async def readCurrent(current: Current, iteration_count):

    message = f'[{iteration_count}] '
    message += "Current : "
    current1 = current.read_modbus(0) / 1000
    current2 = current.read_modbus(1) / 1000
    i = [current.read_modbusbit(0), current.read_modbusbit(1)]

    if current1 + current2 < 10:
        message += "0 mA"
    elif current1 + current2 > 40500:
        message += "0 mA"
    else:
        message += str(current1) + "mA | " + str(current2) + "mA"

    print(message)
    await asyncio.sleep(0)
    return current1, current2, i

async def readVoltage(voltage: Voltage, iteration_count):

    message = f'[{iteration_count}] '
    message += "Voltage : "
    voltage1 = voltage.read_modbus(0) / 1000
    voltage2 = voltage.read_modbus(1) / 1000
    v = [voltage.read_modbusbit(0), voltage.read_modbusbit(1)]

    if voltage1 + voltage2 < 25:
        message += "0 V"
    elif voltage1 + voltage2 > 20200:
        message += "0 V"
    else:
        message += str(voltage1) + " V | " + str(voltage2) + " V"

    print(message)
    await asyncio.sleep(0)
    return voltage1, voltage2, v

async def readRelay(relay: Relay, iteration_count):

    relay_values = []

    for i in range(14):

        relay_values.append(relay.read_modbusbit(i))

    relay_values_str = list(map(str, relay_values))
    message = f'[{iteration_count}]' + " | " + ' | '.join(relay_values_str) + " |"

    print(message)
    await asyncio.sleep(0)
    return relay_values_str

async def read_volatage_current_relay(voltage_relay,current_relay,iteration_count):

    message = f'[{iteration_count}]' + " | " + ' | '.join(list(map(str,current_relay))) + " | " + ' | '.join(list(map(str,voltage_relay))) + " |"
    print(message)

async def execute_relay(relay, n):

    for i in range(0, 14):
        relay.write_modbus(i, n)

async def execute(choice):

    global relay,current,voltage,fourrelay

    await asyncio.sleep(1)

    if choice == 1:

        relay.connect_device()
        await execute_relay(relay, 1)

    elif choice == 0:

        relay.connect_device()
        await execute_relay(relay, 0)

    elif choice >= 80:

        relay.connect_device()
        dat = relay.read_modbusbit(choice-80)
        await asyncio.sleep(0.1)
        relay.write_modbus(choice-80,not dat)

    elif choice >= 70:

        voltage.connect_device()
        dat = voltage.read_modbusbit(choice-70)
        await asyncio.sleep(0.1)
        voltage.write_modbus(choice-70,not dat)

    elif choice >= 60:

        current.connect_device()
        dat = current.read_modbusbit(choice-60)
        await asyncio.sleep(0.1)
        current.write_modbus(choice-60,not dat)

    elif choice >= 20:

        fourrelay.connect_device()
        await asyncio.sleep(0.1)
        fourrelay.write_modbus(choice-20,1)

    elif choice >= 10:

        fourrelay.connect_device()
        await asyncio.sleep(0.1)
        fourrelay.write_modbus(choice-10,0)

    with open("data.txt","w") as f:
        f.write("-1")

    await asyncio.sleep(1)

def menu(choice):

    with open("data.txt","w") as f:
        f.write(str(choice))

async def count():

    mqt2 = Mqt2()
    await asyncio.sleep(1)

async def initialize():

    try:

        time.sleep(3)

        mqtt = Mqtt()
        time.sleep(2)

        print("Ready")

        task1 = asyncio.create_task(begin(current, voltage, relay, mqtt))
        task2 = asyncio.create_task(count())
        results = await asyncio.gather(task1, task2)

        return results

    except serial.serialutil.SerialException as e:

        print('Modbus Connection Error. Check the connection port of the modbus connector or the device port connected to modbus.')
        file_handler = logging.FileHandler('example.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.error("Port Error. Most likely Modbus unplugged or device drivers not allowing serial communication. Error message :  " + str(e))
        time.sleep(2)

if __name__ == '__main__':
    asyncio.run(initialize())
