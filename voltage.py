import minimalmodbus
from configuration import Configuration


class Voltage():
    __modbus_instance = None
    configs:dict = None
    
    def __new__(cls) -> None:
        if not hasattr(cls, 'instance') or cls.instance is None:
            Voltage.configs = Configuration().get_configs('Voltage')
            Voltage.connect_device()
            cls.instance = super(Voltage, cls).__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls):
        cls.instance = None


    @staticmethod
    def connect_device() -> None:
        try:
            Voltage.__modbus_instance = minimalmodbus.Instrument(Voltage.configs['port'], Voltage.configs['slave'], debug = Voltage.configs['debug'])
            Voltage.__modbus_instance.serial.baudrate = Voltage.configs['baudrate']
            Voltage.__modbus_instance.serial.bytesize = Voltage.configs['bytesize']
            Voltage.__modbus_instance.serial.parity   = minimalmodbus.serial.PARITY_NONE
            Voltage.__modbus_instance.serial.stopbits = Voltage.configs['stopbits']
            Voltage.__modbus_instance.serial.timeout  = Voltage.configs['timeout']
            Voltage.__modbus_instance.mode = minimalmodbus.MODE_RTU
        except minimalmodbus.ModbusException as e:
            print("Unable to instantiate modbus", e)

    @staticmethod
    def read_modbus(register_address:int)->int:
        try:
            return Voltage.__modbus_instance.read_register(register_address,0,Voltage.configs['fncode_read'],Voltage.configs['signed'])
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)

    @staticmethod
    def write_modbus(register_address:int, value:int)->int:
        try:
            Voltage.__modbus_instance.write_bit(register_address, value,5)
        except minimalmodbus.ModbusException as e:
            print("Unable to write to slave", e)

    @staticmethod
    def read_modbusbit(register_address:int)->int:
        try:
            return Voltage.__modbus_instance.read_bit(register_address,2)
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)
