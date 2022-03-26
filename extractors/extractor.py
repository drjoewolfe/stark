from selenium import webdriver
from termcolor import colored

import stock_info
from extractors.money_control_extractor import extract_money_control
from extractors.money_control_extractor import extract_money_control_for_request
from extractors.value_research_extractor import extract_value_research
from extractors.ticker_tape_extractor import extract_ticker_tape
from extractors.ticker_tape_extractor import extract_ticker_tape_for_request
from extractors.money_works_4me_extractor import extract_money_works_4me


def extract_stocks(stark_config, stark_input):
    chrome_driver_path = stark_config["system"]["chrome_driver_location"]
    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.maximize_window()

    stock_extract_symbols = stark_input["stock_extract_symbols"]
    extractors_to_run = stark_input["extractors_to_run"]
    stock_extract_configuration_map = get_stock_extract_configuration_map(stark_config)

    extracts = []
    stock_extract_configurations = []

    for extract_symbol in stock_extract_symbols:
        stock_extract_configurations.append(stock_extract_configuration_map[extract_symbol])

    counter, size = 1, len(stock_extract_configurations)
    for configuration in stock_extract_configurations:
        symbol = configuration["symbol"]
        print(f"\t[{counter} / {size}] " + configuration["symbol"])

        info = stock_info.StockInfo()
        info.symbol = symbol
        for extractor_name in extractors_to_run:
            if extractor_name == "money_control":
                print(f"\t\tExtracting " + configuration["symbol"] + " from money-control")
                try:
                    money_control_info = extract_money_control_for_request(browser, configuration)
                    info.merge(money_control_info)
                    print(colored(f"\t\t\tExtraction successful for {symbol}", "green"))
                except Exception as e:
                    print(colored(f"\t\t\tError extracting {symbol}. Skipping...", "red"))
                    print("\t\t\t" + repr(e))

            elif extractor_name == "ticker_tape":
                print(f"\t\tExtracting " + configuration["symbol"] + " from ticker-tape")
                try:
                    ticker_tape_info = extract_ticker_tape_for_request(browser, configuration)
                    info.merge(ticker_tape_info)
                    print(colored(f"\t\t\tExtraction successful for {symbol}", "green"))
                except Exception as e:
                    print(colored(f"\t\t\tError extracting {symbol}. Skipping...", "red"))
                    print("\t\t\t" + repr(e))

        extracts.append(info)
        counter += 1

    return extracts


def get_stock_extract_configuration_map(stark_config):
    stock_extract_configuration_map = {}

    stock_extract_configurations = stark_config["stock_extract_configurations"]

    for configuration in stock_extract_configurations:
        stock_extract_configuration_map[configuration["symbol"]] = configuration

    return stock_extract_configuration_map


def extract(stark_config, stock_extract_configuration_map, stock_extract_symbols):
    chrome_driver_path = stark_config["DEFAULT"]["ChromeDriverLocation"]
    # browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(executable_path=r"D:\Code\modules\chromedriver_win32\chromedriver.exe")
    browser.maximize_window()

    money_control_extracts = extract_money_control(browser, stark_config, stock_extract_configuration_map, stock_extract_symbols)
    # value_research_extracts = extract_value_research(browser, stark_config, stark_input)
    ticker_tape_extracts = extract_ticker_tape(browser, stark_config, stock_extract_configuration_map, stock_extract_symbols)
    # money_works_4me_extracts = extract_money_works_4me(browser, stark_config, stark_input)

    # extracts = merge(money_control_extracts,
    #                  value_research_extracts,
    #                  ticker_tape_extracts,
    #                  money_works_4me_extracts)

    extracts = merge(money_control_extracts,
                     ticker_tape_extracts)

    # extracts = merge(ticker_tape_extracts)

    stark_output = []
    for k, v in extracts.items():
        stark_output.append(v)

    browser.close()

    return stark_output


def extract_symbols(browser, stark_config, stock_extract_configuration_map, stock_extract_symbols):
    extracts = {}

    stock_extract_configurations = []
    for extract_symbol in stock_extract_symbols:
        stock_extract_configurations.append(stock_extract_configuration_map[extract_symbol])

    counter, size = 1, len(stock_extract_configurations)
    for configuration in stock_extract_configurations:
        symbol = configuration["symbol"]
        print(f"\t[{counter} / {size}] " + configuration["symbol"])
        try:
            extracts[symbol] = extract_money_control_for_request(browser, configuration, stark_config)
            print(colored(f"\t\tExtraction successful for {symbol}", "green"))
        except Exception as e:
            print(colored(f"\t\tError extracting {symbol}. Skipping...", "red"))
            print("\t\t" + repr(e))
        counter += 1

    return extracts


def merge(*argv):
    merged = {}
    for arg in argv:
        for k, v in arg.items():
            if k in merged:
                merged[k].merge(v)
            else:
                merged[k] = v

    return merged
