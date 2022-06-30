import concurrent.futures
import threading

from selenium import webdriver
from termcolor import colored

from library import stock_info
from library import extraction_summary
from library.attempt_info import AttemptInfo
from library.run_request import RunRequest
from library.task_info import TaskInfo
from library.timer import Timer
from extractors.money_control_extractor import extract_money_control
from extractors.money_control_extractor import extract_money_control_for_request
from extractors.ticker_tape_extractor import extract_ticker_tape
from extractors.ticker_tape_extractor import extract_ticker_tape_for_request

task_colors = ["cyan", "blue", "magenta", "green", "red"]


def run_extractors(stark_config, stark_input):
    symbols_to_extract = stark_input["symbols_to_extract"]
    extractors_to_run = stark_input["extractors_to_run"]
    parallelism = stark_config["system"]["parallelism"]
    if parallelism > 5:
        parallelism = 5
    if len(symbols_to_extract) < parallelism:
        parallelism = len(symbols_to_extract)

    requests = generate_run_requests(symbols_to_extract, extractors_to_run, parallelism)

    run_summary = extraction_summary.ExtractionSummary()
    futures = []
    counter = 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for run_request in requests:
            task_info = TaskInfo()
            task_info.task_identifier = f"Task - {counter}"
            task_info.task_number = counter
            future = executor.submit(run_extractors_async, stark_config, run_request, task_info)
            futures.append(future)
            counter += 1

    for f in futures:
        run_summary.merge(f.result())

    return run_summary


def run_extractors_async(stark_config, run_request: RunRequest, task_info: TaskInfo):
    run_timer = Timer()
    attempt_timer = Timer()
    execution_timer = Timer()

    symbols_to_extract = run_request.symbols_to_extract
    extractors_to_run = run_request.extractors_to_run

    max_retry_counts = stark_config["system"]["max_retry_counts"]
    attempt_number = 1

    run_summary = extraction_summary.ExtractionSummary()
    run_timer.start()

    while attempt_number <= max_retry_counts:
        attempt_info = AttemptInfo(f"Attempt - {attempt_number}", attempt_number)
        attempt_timer.start()
        log(f"Extractor run - Attempt {attempt_info.attempt_number}", task_info, attempt_info)
        attempt_summary = run_selected_extractors(stark_config, symbols_to_extract, extractors_to_run, run_timer,
                                                  attempt_timer, execution_timer, task_info, attempt_info)

        run_summary.extracts += attempt_summary.extracts
        run_summary.succeeded_symbols += attempt_summary.succeeded_symbols
        run_summary.failed_symbols.clear()
        run_summary.failed_symbols += attempt_summary.failed_symbols

        attempt_timer.stop()
        log(f"Attempt {attempt_number} complete ({attempt_timer.elapsed_formatted()})", task_info, attempt_info, 1)

        if len(attempt_summary.failed_symbols) == 0:
            break

        symbols_to_extract.clear()
        symbols_to_extract += attempt_summary.failed_symbols
        attempt_number += 1

    run_timer.stop()
    log(f"Extraction runs complete ({run_timer.elapsed_formatted()})", task_info)

    return run_summary


def generate_run_requests(symbols_to_extract, extractors_to_run, parallelism):
    total_symbols = len(symbols_to_extract)
    partition_size = int(total_symbols / parallelism)

    print(f"\tSymbols: {total_symbols}, Parallelism: {parallelism}, Partition size: {partition_size}")

    requests = []
    index = 0
    for i in range(0, parallelism):
        symbols = []
        for j in range(0, partition_size):
            symbols.append(symbols_to_extract[index])
            index += 1

        if i == (parallelism - 1):
            # Add all remaining symbols to the last bucket
            while index < len(symbols_to_extract):
                symbols.append(symbols_to_extract[index])
                index += 1

        run_request = RunRequest()
        run_request.symbols_to_extract.extend(symbols)
        run_request.extractors_to_run.extend(extractors_to_run)

        requests.append(run_request)

    return requests


def run_selected_extractors(stark_config, symbols_to_extract, extractors_to_run, run_timer, attempt_timer,
                            execution_timer, task_info: TaskInfo, attempt_info: AttemptInfo):
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

        log(f"[{counter} / {size}] " + configuration["symbol"], task_info, attempt_info, 2)

        info = stock_info.StockInfo()
        info.symbol = symbol
        succeeded = True
        for extractor_name in extractors_to_run:
            if extractor_name == "money_control":
                log(f"Extracting " + title + " from money-control", task_info, attempt_info, 3)
                if not execute_extractor(extract_money_control_for_request, browser, configuration, info, run_timer,
                                         attempt_timer, execution_timer, task_info, attempt_info):
                    succeeded = False
                    break

            elif extractor_name == "ticker_tape":
                log(f"Extracting " + title + " from ticker-tape", task_info, attempt_info, 3)
                if not execute_extractor(extract_ticker_tape_for_request, browser, configuration, info, run_timer,
                                         attempt_timer, execution_timer, task_info, attempt_info):
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


def execute_extractor(extractor_func, browser, configuration, merged_info, run_timer, attempt_timer, execution_timer,
                      task_info: TaskInfo, attempt_info: AttemptInfo):
    execution_timer.start()

    try:
        symbol = configuration["symbol"]
        extracted_stock_info = extractor_func(browser, configuration)
        merged_info.merge(extracted_stock_info)
        execution_timer.stop()
        log(colored(f"Extraction successful for {symbol}",
                    "green") + f" (Current: {execution_timer.elapsed_formatted()}, Attempt: {attempt_timer.elapsed_formatted()}, Run: {run_timer.elapsed_formatted()})",
            task_info, attempt_info, 4)
        return True
    except Exception as e:
        execution_timer.stop()
        log(colored(f"Error extracting {symbol}. Skipping...",
                    "red") + f" (Current: {execution_timer.elapsed_formatted()}, Attempt: {attempt_timer.elapsed_formatted()}, Run: {run_timer.elapsed_formatted()})",
            task_info, attempt_info, 4)
        log(repr(e), task_info, attempt_info, 4)
        return False


def get_stock_extract_configuration_map(stark_config):
    stock_extract_configuration_map = {}

    stock_extract_configurations = stark_config["stock_extract_configurations"]

    for configuration in stock_extract_configurations:
        stock_extract_configuration_map[configuration["symbol"]] = configuration

    return stock_extract_configuration_map


def log(string, task_info: TaskInfo = None, attempt_info: AttemptInfo = None, intend=0):
    color = task_colors[(task_info.task_number - 1) % 5]
    log_string = ""
    if task_info is not None:
        log_string += colored(f"[{task_info.task_identifier}] ", color)
    if attempt_info is not None:
        log_string += colored(f"[{attempt_info.attempt_identifier}] ", "yellow")
    for x in range(0, intend):
        log_string += "\t"
    log_string += f"{string}"
    print(log_string)


def extract(stark_config, stock_extract_configuration_map, stock_extract_symbols):
    chrome_driver_path = stark_config["DEFAULT"]["ChromeDriverLocation"]
    # browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(executable_path=r"D:\Code\modules\chromedriver_win32\chromedriver.exe")
    browser.maximize_window()

    money_control_extracts = extract_money_control(browser, stark_config, stock_extract_configuration_map,
                                                   stock_extract_symbols)
    # value_research_extracts = extract_value_research(browser, stark_config, stark_input)
    ticker_tape_extracts = extract_ticker_tape(browser, stark_config, stock_extract_configuration_map,
                                               stock_extract_symbols)
    # money_works_4me_extracts = extract_money_works_4me(browser, stark_config, stark_input)

    extracts = merge(money_control_extracts,
                     ticker_tape_extracts)

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
