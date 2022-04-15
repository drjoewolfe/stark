from selenium import webdriver
from termcolor import colored

from library import stock_info
from library import extraction_summary
from library.timer import Timer
from extractors.money_control_extractor import extract_money_control
from extractors.money_control_extractor import extract_money_control_for_request
from extractors.ticker_tape_extractor import extract_ticker_tape
from extractors.ticker_tape_extractor import extract_ticker_tape_for_request

run_timer = Timer()
attempt_timer = Timer()
execution_timer = Timer()

def run_extractors(stark_config, stark_input):
    symbols_to_extract = stark_input["symbols_to_extract"]
    extractors_to_run = stark_input["extractors_to_run"]

    max_retry_counts = stark_config["system"]["max_retry_counts"]
    attempt_number = 1

    run_summary = extraction_summary.ExtractionSummary()
    run_timer.start()

    while attempt_number <= max_retry_counts:
        attempt_timer.start()
        print(f"\n\tExtractor run - Attempt {attempt_number}")
        attempt_summary = run_selected_extractors(stark_config, symbols_to_extract, extractors_to_run)

        run_summary.extracts += attempt_summary.extracts
        run_summary.succeeded_symbols += attempt_summary.succeeded_symbols
        run_summary.failed_symbols.clear()
        run_summary.failed_symbols += attempt_summary.failed_symbols

        attempt_timer.stop()
        print(f"\tAttempt {attempt_number} complete ({attempt_timer.elapsed():0.2f} seconds)")

        if len(attempt_summary.failed_symbols) == 0:
            break

        symbols_to_extract.clear()
        symbols_to_extract += attempt_summary.failed_symbols
        attempt_number += 1

    run_timer.stop()
    print(f"\nExtraction runs complete ({run_timer.elapsed():0.2f} seconds)")

    return run_summary


def run_selected_extractors(stark_config, symbols_to_extract, extractors_to_run):
    chrome_driver_path = stark_config["system"]["chrome_driver_location"]
    browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser.maximize_window()

    stock_extract_configuration_map = get_stock_extract_configuration_map(stark_config)

    summary = extraction_summary.ExtractionSummary()
    summary.symbols_to_extract += symbols_to_extract

    extracts = summary.extracts
    succeeded_symbols = summary.succeeded_symbols
    failed_symbols = summary.failed_symbols

    stock_extract_configurations = []

    for extract_symbol in symbols_to_extract:
        stock_extract_configurations.append(stock_extract_configuration_map[extract_symbol])

    counter, size = 1, len(stock_extract_configurations)
    for configuration in stock_extract_configurations:
        symbol = configuration["symbol"]
        company = configuration["company"]
        title = symbol
        if company:
            title += " (" + company + ")"

        print(f"\t\t[{counter} / {size}] " + configuration["symbol"])

        info = stock_info.StockInfo()
        info.symbol = symbol
        succeeded = True
        for extractor_name in extractors_to_run:
            if extractor_name == "money_control":
                print(f"\t\t\tExtracting " + title + " from money-control")
                if not execute_extractor(extract_money_control_for_request, browser, configuration, info):
                    succeeded = False
                    break

            elif extractor_name == "ticker_tape":
                print(f"\t\t\tExtracting " + title + " from ticker-tape")
                if not execute_extractor(extract_ticker_tape_for_request, browser, configuration, info):
                    succeeded = False
                    break

        if succeeded:
            extracts.append(info)
            succeeded_symbols.append(symbol)
        else:
            failed_symbols.append(symbol)

        counter += 1

    browser.close()
    return summary


def execute_extractor(extractor_func, browser, configuration, merged_info):
    execution_timer.start()

    try:
        symbol = configuration["symbol"]
        extracted_stock_info = extractor_func(browser, configuration)
        merged_info.merge(extracted_stock_info)
        execution_timer.stop()
        print(colored(f"\t\t\t\tExtraction successful for {symbol}", "green") + f" (Current: {execution_timer.elapsed():0.2f}s, Attempt: {attempt_timer.elapsed():0.2f}s, Run: {run_timer.elapsed():0.2f}s)")
        return True
    except Exception as e:
        execution_timer.stop()
        print(colored(f"\t\t\t\tError extracting {symbol}. Skipping...", "red") + f" (Current: {execution_timer.elapsed():0.2f}s, Attempt: {attempt_timer.elapsed():0.2f}s, Run: {run_timer.elapsed():0.2f}s)")
        print("\t\t\t\t" + repr(e))
        return False


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


def merge(*argv):
    merged = {}
    for arg in argv:
        for k, v in arg.items():
            if k in merged:
                merged[k].merge(v)
            else:
                merged[k] = v

    return merged
