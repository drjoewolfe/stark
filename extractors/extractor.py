from selenium import webdriver

from extractors.money_control_extractor import extract_money_control


def extract(stark_config, stark_input):
    chrome_driver_path = stark_config["DEFAULT"]["ChromeDriverLocation"]
    # browser = webdriver.Chrome(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(executable_path=r"D:\Code\modules\chromedriver_win32\chromedriver.exe")
    browser.maximize_window()

    money_control_extracts = extract_money_control(browser, stark_config, stark_input)
    value_research_extracts = extract_money_control(browser, stark_config, stark_input)
    ticker_tape_extracts = extract_money_control(browser, stark_config, stark_input)
    money_works_4me_extracts = extract_money_control(browser, stark_config, stark_input)

    extracts = merge(money_control_extracts,
                     value_research_extracts,
                     ticker_tape_extracts,
                     ticker_tape_extracts)

    stark_output = []
    for k, v in money_control_extracts.items():
        stark_output.append(v)
    #
    # for stock_info_request in stark_input["stock_info_requests"]:
    #     extract_money_control(browser, stock_info_request, stark_input, stark_output)

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
