from selenium import webdriver

from extractors.money_control_extractor import extract_money_control
from extractors.value_research_extractor import extract_value_research
from extractors.ticker_tape_extractor import extract_ticker_tape
from extractors.money_works_4me_extractor import extract_money_works_4me


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
