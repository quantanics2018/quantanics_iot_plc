import minimalmodbus
from configuration import Configuration


class Modbus():
    __modbus_instance = None
    configs:dict = None
    
    def __new__(cls) -> None:
        if not hasattr(cls, 'instance') or cls.instance is None:
            Modbus.configs = Configuration().get_configs('Modbus')
            cls.instance = super(Modbus, cls).__new__(cls)
        return cls.instance

    @classmethod
    def clear(cls):
        cls.instance = None


    @staticmethod
    def connect_device() -> None:
        try:
            Modbus.__modbus_instance = minimalmodbus.Instrument(Modbus.configs['port'], Modbus.configs['slave'], debug = Modbus.configs['debug'])
            Modbus.__modbus_instance.serial.baudrate = Modbus.configs['baudrate']
            Modbus.__modbus_instance.serial.bytesize = Modbus.configs['bytesize']
            Modbus.__modbus_instance.serial.parity   = minimalmodbus.serial.PARITY_NONE
            Modbus.__modbus_instance.serial.stopbits = Modbus.configs['stopbits']
            Modbus.__modbus_instance.serial.timeout  = Modbus.configs['timeout']
            Modbus.__modbus_instance.mode = minimalmodbus.MODE_RTU
        except minimalmodbus.ModbusException as e:
            print("Unable to instantiate modbus", e)

    @staticmethod
    def read_modbus(register_address:int)->int:
        return Modbus.__modbus_instance.read_register(register_address,0,Modbus.configs['fncode_read'],Modbus.configs['signed'])

    @staticmethod
    def write_modbus(register_address:int, value:int)->int:
        Modbus.__modbus_instance.write_bit(register_address, value,5)

    @staticmethod
    def read_modbusbit(register_address:int)->int:
        return Modbus.__modbus_instance.read_bit(register_address,2)
