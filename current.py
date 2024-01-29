import minimalmodbus
from configuration import Configuration


class Current():
    __modbus_instance = None
    configs:dict = None
    
    def __new__(cls) -> None:
        if not hasattr(cls, 'instance') or cls.instance is None:
            Current.configs = Configuration().get_configs('Current')
            Current.connect_device()
            cls.instance = super(Current, cls).__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls):
        cls.instance = None


    @staticmethod
    def connect_device() -> None:
        try:
            Current.__modbus_instance = minimalmodbus.Instrument(Current.configs['port'], Current.configs['slave'], debug = Current.configs['debug'])
            Current.__modbus_instance.serial.baudrate = Current.configs['baudrate']
            Current.__modbus_instance.serial.bytesize = Current.configs['bytesize']
            Current.__modbus_instance.serial.parity   = minimalmodbus.serial.PARITY_NONE
            Current.__modbus_instance.serial.stopbits = Current.configs['stopbits']
            Current.__modbus_instance.serial.timeout  = Current.configs['timeout']
            Current.__modbus_instance.mode = minimalmodbus.MODE_RTU
        except minimalmodbus.ModbusException as e:
            print("Unable to instantiate modbus", e)

    @staticmethod
    def read_modbus(register_address:int)->int:
        try:
            return Current.__modbus_instance.read_register(register_address,0,Current.configs['fncode_read'],Current.configs['signed'])
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)

    @staticmethod
    def write_modbus(register_address:int, value:int)->int:
        try:
            Current.__modbus_instance.write_bit(register_address, value,5)
        except minimalmodbus.ModbusException as e:
            print("Unable to write to slave", e)

    @staticmethod
    def read_modbusbit(register_address:int)->int:
        try:
            return Current.__modbus_instance.read_bit(register_address,2)
        except minimalmodbus.ModbusException as e:
            print("Unable to read from slave", e)
