from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from utilities import *
import StockInfo

browser = None

def extract_money_control(stock_info_request, stark_config, stark_output):
    global browser

    search_term = stock_info_request["symbol"]
    if "mc_search_term" in stock_info_request:
        search_term = stock_info_request["mc_search_term"]

    try:
        browser.get("https://www.moneycontrol.com/india/stockpricequote/")
        search_box = browser.find_element(By.ID, "company")
        search_box.send_keys(search_term)
        time.sleep(2)
        go_button = search_box.find_element(By.XPATH, "../input[2]")
        go_button.click()

        info = StockInfo.StockInfo()

        info.symbol = stock_info_request["symbol"]
        info.name = browser.find_element(By.XPATH, "//div[@id='stockName']/h1").text
        info.sector = browser.find_element(By.XPATH, "//div[@id='stockName']/span/strong/a").text
        info.price = get_decimal(browser.find_element(By.ID, "nsespotval").get_attribute("value"))
        info.day_open_price = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Open')]/../td[2]").text)
        info.day_previous_close_price = get_decimal(browser.find_element(By.XPATH,
                                                             "//td[contains(text(), 'Previous Close')]/../td[2]").text)
        info.volume = get_int(browser.find_element(By.XPATH, "//td[contains(text(), 'Volume')]/../td[2]").text)
        info.value_lakhs = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Value (Lacs)')]/../td[2]").text)
        info.vwap = get_decimal(browser.find_element(By.XPATH, "//td[contains(@class, 'nsevwap')]").text)
        info.beta = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Beta')]/../td[2]").text)
        info.day_high_price = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'High')]/../td[2]").text)
        info.day_low_price = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Low')]/../td[2]").text)
        info.uc_limit = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'UC Limit')]/../td[2]").text)
        info.lc_limit = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'LC Limit')]/../td[2]").text)
        info.week_52_high = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), '52 Week High')]/../td[2]").text)
        info.week_52_low = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), '52 Week Low')]/../td[2]").text)
        info.ttm_eps = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'TTM EPS')]/../td[2]").text)
        info.ttm_pe = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'TTM PE')]/../td[2]").text)
        info.sector_pe = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Sector PE')]/../td[2]").text)
        info.book_value_per_share = get_decimal(browser.find_element(By.XPATH,
                                                         "//td[contains(text(), 'Book Value Per Share')]/../td[2]").text)
        info.pb = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'P/B')]/../td[2]").text)
        info.face_value = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Face Value')]/../td[2]").text)
        info.market_cap_crores = get_decimal(browser.find_element(By.XPATH,
                                                      "//td[contains(text(), 'Mkt Cap (Rs. Cr.)')]/../td[2]").text)
        info.dividend_yeild = get_decimal(browser.find_element(By.XPATH, "//td[contains(text(), 'Dividend Yield')]/../td[2]").text)
        info.avg_volume_20D = get_int(browser.find_element(By.XPATH, "//td[contains(text(), '20D Avg Volume')]/../td[2]").text)
        info.avg_delivery_percent_20D = get_decimal(browser.find_element(By.XPATH,
                                                             "//td[contains(text(), '20D Avg Delivery(%)')]/../td[2]").text)

        stark_output.append(info)
        print("Extracted " + stock_info_request["symbol"] + " from money-control")
    except Exception as e:
        print("Error extracting " + stock_info_request["symbol"] + ". Skipping...")
        print(e)


def extract(stark_config, stark_input):
    global browser

    chrome_driver_path = stark_config["DEFAULT"]["ChromeDriverLocation"]
    # browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(executable_path=r"D:\Code\modules\chromedriver_win32\chromedriver.exe")
    browser.maximize_window()

    stark_output = []
    for stock_info_request in stark_input["stock_info_requests"]:
        extract_money_control(stock_info_request, stark_input, stark_output)

    browser.close()

    return stark_output