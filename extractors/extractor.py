from selenium import webdriver

from extractors.money_control_extractor import extract_money_control


def extract(stark_config, stark_input):
    chrome_driver_path = stark_config["DEFAULT"]["ChromeDriverLocation"]
    # browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(executable_path=r"D:\Code\modules\chromedriver_win32\chromedriver.exe")
    browser.maximize_window()

    stark_output = []
    for stock_info_request in stark_input["stock_info_requests"]:
        extract_money_control(browser, stock_info_request, stark_input, stark_output)

    browser.close()

    return stark_output
