import configparser
import json


def load_config():
    stark_config = configparser.ConfigParser()
    stark_config.read('conf/stark.ini')

    return stark_config


def load_input():
    with open("conf/input.json", "r") as input_file:
        stark_input = json.load(input_file)
        input_file.close()

    return stark_input
