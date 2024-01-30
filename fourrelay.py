import minimalmodbus
from configuration import Configuration


class fourRelay():
    __modbus_instance = None
    configs:dict = None
    
    def __new__(cls) -> None:
        if not hasattr(cls, 'instance') or cls.instance is None:
            fourRelay.configs = Configuration().get_configs('fourRelay')
            fourRelay.connect_device()
            cls.instance = super(fourRelay, cls).__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls):
        cls.instance = None


    @staticmethod
    def connect_device() -> None:
        try:
            fourRelay.__modbus_instance = minimalmodbus.Instrument(fourRelay.configs['port'], fourRelay.configs['slave'], debug = fourRelay.configs['debug'])
            fourRelay.__modbus_instance.serial.baudrate = fourRelay.configs['baudrate']
            fourRelay.__modbus_instance.serial.bytesize = fourRelay.configs['bytesize']
            fourRelay.__modbus_instance.serial.parity   = minimalmodbus.serial.PARITY_NONE
            fourRelay.__modbus_instance.serial.stopbits = fourRelay.configs['stopbits']
            fourRelay.__modbus_instance.serial.timeout  = fourRelay.configs['timeout']
            fourRelay.__modbus_instance.mode = minimalmodbus.MODE_RTU
        except minimalmodbus.ModbusException as e:
            print("Unable to instantiate modbus", e)

    @staticmethod
    def read_modbus(register_address:int)->int:
        try:
            return fourRelay.__modbus_instance.read_register(register_address,0,fourRelay.configs['fncode_read'],fourRelay.configs['signed'])
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)

    @staticmethod
    def write_modbus(register_address:int, value:int)->int:
        try:
            fourRelay.__modbus_instance.write_bit(register_address, value,5)
        except minimalmodbus.ModbusException as e:
            print("Unable to write to slave", e)

    @staticmethod
    def read_modbusbit(register_address:int)->int:
        try:
            return fourRelay.__modbus_instance.read_bit(register_address,1)
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)
