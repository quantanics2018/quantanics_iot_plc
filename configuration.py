import toml


class MqttCallbackConfiguration:
    def on_message(client, userdata, msg):
        Configuration.update_configs("new",{"as":"vs"})


class Configuration():
    __config_instance:dict = None
    config_file_path:str = 'config.toml'
    config_read_mode:str = 'r'
    config_write_mode:str = 'w'

    def __new__(cls) -> None:
        if not hasattr(cls, 'instance'):
            Configuration.load_configuration()
            if Configuration.__config_instance != None:
                cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance
    
    def clear(cls):
        cls.instance = None

    @staticmethod
    def load_configuration() -> None:
        try:
            with open(Configuration.config_file_path, Configuration.config_read_mode) as configs:
                Configuration.__config_instance = toml.load(configs)
        except:
            print("Unable to load configuration")

    @staticmethod
    def get_configs(class_ref:str)-> dict:
        return Configuration.__config_instance[class_ref]
    
    @staticmethod
    def update_configs(class_ref:str, configs:dict)-> None:
        Configuration.__config_instance[class_ref] = configs
        with open(Configuration.config_file_path, Configuration.config_write_mode) as configs:
            toml.dump(Configuration.__config_instance,configs)
        return
