import configparser

# Method to read config file settings
def read_config(path):
    config = configparser.ConfigParser()
    print("read config from file: " + path)
    config.read(path)
    return config