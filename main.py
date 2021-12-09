import configparser
import json
from extractor import *


def load_config():
    stark_config = configparser.ConfigParser()
    stark_config.read('conf/stark.ini')

    return stark_config


def load_input():
    with open("conf/input.json", "r") as input_file:
        stark_input = json.load(input_file)
        input_file.close()

    return stark_input


def generate_output(stark_output):
    with open('out/stark_output.csv', 'w') as csvfile:
        header = "symbol, name, sector, price, day_open_price, day_previous_close_price, volume, value_lakhs, vwap, beta, day_high_price, day_low_price, uc_limit, lc_limit, week_52_high, " \
                 "week_52_low, ttm_eps, ttm_pe, sector_pe, book_value_per_share, pb, face_value, market_cap_crores, dividend_yeild, avg_volume_20D, avg_delivery_percent_20D"

        csvfile.writelines(header)
        csvfile.write("\n")

        for info in stark_output:
            record = info.symbol + ", " \
                     + info.name + ", " \
                     + info.sector + ", " \
                     + str(info.price) + ", " \
                     + str(info.day_open_price) + ", " \
                     + str(info.day_previous_close_price) + ", " \
                     + str(info.volume) + ", " \
                     + str(info.value_lakhs) + ", " \
                     + str(info.vwap) + ", " \
                     + str(info.beta) + ", " \
                     + str(info.day_high_price) + ", " \
                     + str(info.day_low_price) + ", " \
                     + str(info.uc_limit) + ", " \
                     + str(info.lc_limit) + ", " \
                     + str(info.week_52_high) + ", " \
                     + str(info.week_52_low) + ", " \
                     + str(info.ttm_eps) + ", " \
                     + str(info.ttm_pe) + ", " \
                     + str(info.sector_pe) + ", " \
                     + str(info.book_value_per_share) + ", " \
                     + str(info.pb) + ", " \
                     + str(info.face_value) + ", " \
                     + str(info.market_cap_crores) + ", " \
                     + str(info.dividend_yeild) + ", " \
                     + str(info.avg_volume_20D) + ", " \
                     + str(info.avg_delivery_percent_20D)

            print(info)
            csvfile.writelines(record)
            csvfile.write("\n")


if __name__ == '__main__':
    stark_config = load_config()
    stark_input = load_input()

    stark_output = extract(stark_config, stark_input)
    generate_output(stark_output)
