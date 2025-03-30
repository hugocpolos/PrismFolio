from prismfolio.wallet import Wallet
from prismfolio.investmentsuggestion import WalletInvestmentSuggestion
from prismfolio import brapi
import json
import argparse
import logging


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_data')
    parser.add_argument('new_investment_value', type=float)
    return parser.parse_args()


def main():
    args = argument_parser()

    with open(args.input_data) as fp:
        input_dict = json.load(fp)

    try:
        wallet = Wallet.from_dict(input_dict)
        wallet.update_asset_values(brapi.get_current_stock_price)
        suggestion = WalletInvestmentSuggestion(wallet, args.new_investment_value)
    except Exception as err:
        logging.error(err)
        return

    print(suggestion)


if __name__ == '__main__':
    main()
