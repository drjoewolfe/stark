from configuration import *
from extractors.extractor import *
from sink import *


if __name__ == '__main__':
    print(f"Preparing for extraction")
    print(f"\tLoading configuration")
    stark_config = load_stark_config()
    # stock_extract_configuration_map = load_stock_extract_configurations()

    print(f"\tLoading input")
    stark_input = load_stark_input()
    # stock_extract_symbols = load_stock_extract_symbols()

    print("")
    print(f"Running extractors")
    # stark_output = extract(stark_config, stock_extract_configuration_map, stock_extract_symbols)
    summary = run_extractors(stark_config, stark_input)

    print("")
    generate_output(summary)

    print("\nExtraction completed")
