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
        time.sleep(2)

        browser.find_element(By.ID, "react-autowhatever-1").find_elements(By.TAG_NAME, "li")[2].click()

        time.sleep(2)
        sector_pe = browser.find_element(By.XPATH, "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector PE\")]/../../../div[2]").text
        sector_pb = browser.find_element(By.XPATH,
                                         "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector PB\")]/../../../div[2]").text
        sector_dividend_yield = browser.find_element(By.XPATH,
                                         "//div[@data-section-tag=\"key-metrics\"]/div/div//span[contains(text(), \"Sector Div Yld\")]/../../../div[2]").text

        info = stock_info.StockInfo()

        info.symbol = stock_info_request["symbol"]
        info.sector_pe = sector_pe
        info.sector_pb = sector_pb
        info.sector_dividend_yield = sector_dividend_yield

        print("Extracted " + stock_info_request["symbol"] + " from ticker-tape")
    except Exception as e:
        print("Error extracting " + stock_info_request["symbol"] + " from ticker-tape. Skipping...")
        print(e)

    return info
