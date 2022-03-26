import configparser
import json
import yaml


def load_stark_config():
    # stark_config = configparser.ConfigParser()
    # stark_config.read('conf/stark.ini')

    with open('conf/stark_configuration.yaml', 'r') as file:
        stark_config = yaml.safe_load(file)

    return stark_config


def load_stark_input():
    with open('conf/stark_input.yaml', 'r') as file:
        stark_input = yaml.safe_load(file)

    return stark_input


def load_stock_extract_configurations():
    stock_extract_configuration_map = {}
    with open("conf/stock_extract_configurations.json", "r") as input_file:
        stock_extract_configurations = json.load(input_file)["stock_extract_configurations"]
        input_file.close()

    for configuration in stock_extract_configurations:
        stock_extract_configuration_map[configuration["symbol"]] = configuration

    return stock_extract_configuration_map


def load_stock_extract_symbols():
    with open("conf/stock_extract_symbols.json", "r") as input_file:
        stock_extract_symbols = json.load(input_file)["stock_extract_symbols"]
        input_file.close()

    return stock_extract_symbols
