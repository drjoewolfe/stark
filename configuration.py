import configparser
import json


def load_stark_config():
    stark_config = configparser.ConfigParser()
    stark_config.read('conf/stark.ini')

    return stark_config


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
