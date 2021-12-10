from configuration import *
from extractor import *
from sink import *


if __name__ == '__main__':
    stark_config = load_config()
    stark_input = load_input()

    stark_output = extract(stark_config, stark_input)
    generate_output(stark_output)
