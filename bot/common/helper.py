import configparser
import os

# get the current working directory
current_working_directory = os.getcwd()
# Method to read config file settings
def read_config(path):
    config = configparser.ConfigParser()
    print("read config from file: " + current_working_directory+"/"+path)
    config.read(current_working_directory+"/"+path)
    return config