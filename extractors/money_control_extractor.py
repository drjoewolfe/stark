import time
from termcolor import colored

from selenium.webdriver.common.by import By

from library import stock_info
from utilities import get_decimal, get_int


def extract_money_control(browser, stark_config, stock_extract_configuration_map, stock_extract_symbols):
    print(f"Money Control (https://www.moneycontrol.com/)")
    extracts = {}

    stock_extract_configurations = []
    for extract_symbol in stock_extract_symbols:
        stock_extract_configurations.append(stock_extract_configuration_map[extract_symbol])

    # stock_info_requests = stark_input["stock_info_requests"]
    counter, size = 1, len(stock_extract_configurations)
    for configuration in stock_extract_configurations:
        symbol = configuration["symbol"]
        print(f"\t[{counter} / {size}] Extracting " + configuration["symbol"] + " from money-control")
        try:
            extracts[symbol] = extract_money_control_for_request(browser, configuration)
            print(colored(f"\t\tExtraction successful for {symbol}", "green"))
        except Exception as e:
            print(colored(f"\t\tError extracting {symbol}. Skipping...", "red"))
            print("\t\t" + repr(e))
        counter += 1

    return extracts


def extract_money_control_for_request(browser, configuration):
    info = None

    # raise IOError("Dummy error..")

    search_term = configuration["mc_search_term"]
    if not search_term:
        search_term = configuration["symbol"]

    browser.get("https://www.moneycontrol.com/india/stockpricequote/")
    search_box = browser.find_element(By.ID, "company")
    search_box.send_keys(search_term)
    time.sleep(2)
    go_button = search_box.find_element(By.XPATH, "../input[2]")
    go_button.click()

    info = stock_info.StockInfo()

    info.symbol = configuration["symbol"]
    info.name = browser.find_element(By.XPATH, "//div[@id='stockName']/h1").text
    info.sector = browser.find_element(By.XPATH, "//div[@id='stockName']/span/strong/a").text
    info.price = get_decimal(browser.find_element(By.ID, "nsespotval").get_attribute("value"))
    info.day_open_price = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'Open')]/../td[2]").text)
    info.day_previous_close_price = get_decimal(browser.find_element(By.XPATH,
                                                                     "//td[contains(text(), 'Previous Close')]/../td[2]").text)
    info.volume = get_int(browser.find_element(By.XPATH, "//td[contains(text(), 'Volume')]/../td[2]").text)
    info.value_lakhs = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'Value (Lacs)')]/../td[2]").text)
    info.vwap = get_decimal(browser.find_element(By.XPATH, "//td[contains(@class, 'nsevwap')]").text)
    info.beta = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Beta')]/../td[2]").text)
    info.day_high_price = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'High')]/../td[2]").text)
    info.day_low_price = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Low')]/../td[2]").text)
    info.uc_limit = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'UC Limit')]/../td[2]").text)
    info.lc_limit = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'LC Limit')]/../td[2]").text)
    info.week_52_high = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), '52 Week High')]/../td[2]").text)
    info.week_52_low = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), '52 Week Low')]/../td[2]").text)
    info.ttm_eps = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'TTM EPS')]/../td[2]").text)
    info.ttm_pe = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'TTM PE')]/../td[2]").text)
    info.sector_pe = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'Sector PE')]/../td[2]").text)
    info.book_value_per_share = get_decimal(browser.find_element(By.XPATH,
                                                                 "//td[contains(text(), 'Book Value Per Share')]/../td[2]").text)
    info.pb = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'P/B')]/../td[2]").text)
    info.face_value = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'Face Value')]/../td[2]").text)
    info.market_cap_crores = get_decimal(browser.find_element(By.XPATH,
                                                              "//td[contains(text(), 'Mkt Cap (Rs. Cr.)')]/../td[2]").text)
    info.dividend_yield = get_decimal(
        browser.find_element(By.XPATH, "//td[contains(text(), 'Dividend Yield')]/../td[2]").text)
    info.avg_volume_20D = get_int(
        browser.find_element(By.XPATH, "//td[contains(text(), '20D Avg Volume')]/../td[2]").text)
    info.avg_delivery_percent_20D = get_decimal(browser.find_element(By.XPATH,
                                                                     "//td[contains(text(), '20D Avg Delivery(%)')]/../td[2]").text)

    return info
