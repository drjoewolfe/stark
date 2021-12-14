import time

from selenium.webdriver.common.by import By

import stock_info
from utilities import get_decimal, get_int


def extract_ticker_tape(browser, stark_config, stark_input):
    extracts = {}
    for stock_info_request in stark_input["stock_info_requests"]:
        symbol = stock_info_request["symbol"]
        extracts[symbol] = extract_ticker_tape_for_request(browser, stock_info_request, stark_config)

    return extracts


def extract_ticker_tape_for_request(browser, stock_info_request, stark_config):
    info = None

    search_term = stock_info_request["symbol"]
    if "tt_search_term" in stock_info_request:
        search_term = stock_info_request["tt_search_term"]

    try:
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
        tt_returns_vs_fd_rates_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Returns vs FD rates')]/../../p").text
        tt_dividend_returns_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Dividend Returns')]/../../p").text
        tt_entry_pont_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Entry Point')]/../../p").text
        tt_red_flags_commentary = browser.find_element(By.XPATH, "//span[contains(text(), 'Red Flag')]/../../p").text

        info = stock_info.StockInfo()

        info.symbol = stock_info_request["symbol"]
        info.sector_pe = sector_pe
        info.sector_pb = sector_pb
        info.sector_dividend_yield = sector_dividend_yield
        info.tt_intrinsic_value_commentary = tt_intrinsic_value_commentary
        info.tt_returns_vs_fd_rates_commentary = tt_returns_vs_fd_rates_commentary
        info.tt_dividend_returns_commentary = tt_dividend_returns_commentary
        info.tt_entry_pont_commentary = tt_entry_pont_commentary
        info.tt_red_flags_commentary = tt_red_flags_commentary

        print("Extracted " + stock_info_request["symbol"] + " from ticker-tape")
    except Exception as e:
        print("Error extracting " + stock_info_request["symbol"] + " from ticker-tape. Skipping...")
        print(e)

    return info
