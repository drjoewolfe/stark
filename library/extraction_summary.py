class ExtractionSummary:
    def __init__(self):
        self.extracts = []
        self.symbols_to_extract = []
        self.succeeded_symbols = []
        self.failed_symbols = []

    def merge(self, other):
        for extract in other.extracts:
            self.extracts.append(extract)

        for symbol in other.symbols_to_extract:
            self.symbols_to_extract.append(symbol)

        for symbol in other.succeeded_symbols:
            self.succeeded_symbols.append(symbol)

        for symbol in other.failed_symbols:
            self.failed_symbols.append(symbol)