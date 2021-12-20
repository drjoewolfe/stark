from configuration import *
from extractors.extractor import *
from sink import *


if __name__ == '__main__':
    print(f"Preparing for extraction")
    print(f"\tLoading configuration")
    stark_config = load_config()

    print(f"\tLoading input")
    stark_input = load_input()

    print("")
    print(f"Running extractors")
    stark_output = extract(stark_config, stark_input)

    print("")
    generate_output(stark_output)

    print("\nExtraction completed")
