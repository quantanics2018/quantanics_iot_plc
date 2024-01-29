import minimalmodbus
from configuration import Configuration


class Relay():
    __modbus_instance = None
    configs:dict = None
    
    def __new__(cls) -> None:
        if not hasattr(cls, 'instance') or cls.instance is None:
            Relay.configs = Configuration().get_configs('Relay')
            Relay.connect_device()
            cls.instance = super(Relay, cls).__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls):
        cls.instance = None


    @staticmethod
    def connect_device() -> None:
        try:
            Relay.__modbus_instance = minimalmodbus.Instrument(Relay.configs['port'], Relay.configs['slave'], debug = Relay.configs['debug'])
            Relay.__modbus_instance.serial.baudrate = Relay.configs['baudrate']
            Relay.__modbus_instance.serial.bytesize = Relay.configs['bytesize']
            Relay.__modbus_instance.serial.parity   = minimalmodbus.serial.PARITY_NONE
            Relay.__modbus_instance.serial.stopbits = Relay.configs['stopbits']
            Relay.__modbus_instance.serial.timeout  = Relay.configs['timeout']
            Relay.__modbus_instance.mode = minimalmodbus.MODE_RTU
        except minimalmodbus.ModbusException as e:
            print("Unable to instantiate modbus", e)

    @staticmethod
    def read_modbus(register_address:int)->int:
        try:
            return Relay.__modbus_instance.read_register(register_address,0,Relay.configs['fncode_read'],Relay.configs['signed'])
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)

    @staticmethod
    def write_modbus(register_address:int, value:int)->int:
        try:
            Relay.__modbus_instance.write_bit(register_address, value,5)
        except minimalmodbus.ModbusException as e:
            print("Unable to write to slave", e)

    @staticmethod
    def read_modbusbit(register_address:int)->int:
        try:
            return Relay.__modbus_instance.read_bit(register_address,2)
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)
