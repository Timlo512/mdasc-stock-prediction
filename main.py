from Data import Data
import yahoo_fin.stock_info as si

import sys

method = sys.argv[1] if len(sys.argv) > 1 else 'async'

def main():

    data = Data()
    args = {}
    fn = si.get_data
    data.get_all_ticker_data(fn, args)

if __name__ == "__main__":
    main()