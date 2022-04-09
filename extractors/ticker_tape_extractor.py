import time
from termcolor import colored
from selenium.webdriver.common.by import By

from library import stock_info


def extract_ticker_tape(browser, stark_config, stock_extract_configuration_map, stock_extract_symbols):
    print(f"Ticker Tape (https://www.tickertape.in/)")
    extracts = {}

    stock_extract_configurations = []
    for extract_symbol in stock_extract_symbols:
        stock_extract_configurations.append(stock_extract_configuration_map[extract_symbol])

    # stock_info_requests = stark_input["stock_info_requests"]
    counter, size = 1, len(stock_extract_configurations)
    for configuration in stock_extract_configurations:
        symbol = configuration["symbol"]
        print(f"\t[{counter} / {size}] Extracting " + configuration["symbol"] + " from ticker-tape")
        try:
            extracts[symbol] = extract_ticker_tape_for_request(browser, configuration)
            print(colored(f"\t\tExtraction successful for {symbol}", "green"))
        except Exception as e:
            print(colored(f"\t\tError extracting {symbol}. Skipping...", "red"))
            print("\t\t" + repr(e))
        counter += 1

    return extracts


def extract_ticker_tape_for_request(browser, configuration):
    info = None

    # raise IOError("Dummy error..")

    search_term = configuration["tt_search_term"]
    if not search_term:
        search_term = configuration["symbol"]

    browser.get("https://www.tickertape.in/")
    search_box = browser.find_element(By.ID, "search-stock-input")
    search_box.send_keys(search_term)
    time.sleep(1)

    search_result_link = browser.find_element(By.XPATH, "//div[@id='react-autowhatever-1']/div//li/div/a").get_attribute("href")
    browser.get(search_result_link)

    time.sleep(1)
    sector_pe = browser.find_element(By.XPATH, "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector PE\")]/../../../div[2]").text
    sector_pb = browser.find_element(By.XPATH,
                                     "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector PB\")]/../../../div[2]").text
    sector_dividend_yield = browser.find_element(By.XPATH,
                                     "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector Div Yld\")]/../../../div[2]").text

    tt_intrinsic_value_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Intrinsic Value')]/../../p").text
    tt_returns_vs_fd_rates_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'ROE vs FD rates')]/../../p").text
    tt_dividend_returns_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Dividend Returns')]/../../p").text
    tt_entry_pont_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Entry Point')]/../../p").text
    tt_red_flags_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Red Flag')]/../../p").text

    info = stock_info.StockInfo()

    info.symbol = configuration["symbol"]
    info.sector_pe = sector_pe
    info.sector_pb = sector_pb
    info.sector_dividend_yield = sector_dividend_yield
    info.tt_intrinsic_value_commentary = tt_intrinsic_value_commentary
    info.tt_returns_vs_fd_rates_commentary = tt_returns_vs_fd_rates_commentary
    info.tt_dividend_returns_commentary = tt_dividend_returns_commentary
    info.tt_entry_pont_commentary = tt_entry_pont_commentary
    info.tt_red_flags_commentary = tt_red_flags_commentary

    return info
