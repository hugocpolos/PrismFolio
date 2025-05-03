import argparse
import json
import logging

from prismfolio import brapi
from prismfolio.investmentsuggestion import WalletInvestmentSuggestion
from prismfolio.wallet import Wallet


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_data')
    parser.add_argument('new_investment_value', type=float)
    parser.add_argument('-d', '--dry-run', action='store_true')
    return parser.parse_args()


def dry_run_function(_):
    return 1.0


def display_suggestion(suggestion: WalletInvestmentSuggestion):
    _display_group_layout = "{}\t Investment: R$ {:5.2f}"
    _table_header = "asset\t| investment\t| quantity\t| unit price\t| left"
    _display_asset_layout = "{}\t| R$ {:5.2f}\t| {:4d} shares\t| R$ {:5.2f}\t| R$ {:5.2f}"
    _available_remainder_layout = "\nTotal remainder: R$ {:5.2f}, suggestion:"

    for group in suggestion:
        if group.get_suggested_investment() == 0:
            continue

        print(_display_group_layout.format(group.get_investment_group().get_name(),
                                           group.get_suggested_investment()))
        print(_table_header)
        for asset in group:
            if asset.get_suggested_investment() == 0:
                continue
            print(_display_asset_layout.format(
                asset.get_asset().get_code().ljust(6),
                asset.get_suggested_investment(),
                int(asset.get_suggested_shares_buying()),
                asset.get_asset().get_price(),
                asset.get_remainder()))


def main():
    args = argument_parser()
    stock_price_acquisition_function = brapi.get_current_stock_price
    stock_price_earning_acquisitiong_function = brapi.get_price_earning

    if args.dry_run:
        stock_price_acquisition_function = dry_run_function
        stock_price_earning_acquisitiong_function = dry_run_function

    with open(args.input_data, encoding="utf-8") as fp:
        input_dict = json.load(fp)

    try:
        wallet = Wallet.from_dict(input_dict)
        wallet.update_asset_values(stock_price_acquisition_function)
        suggestion = WalletInvestmentSuggestion(wallet, args.new_investment_value)
    except Exception as err:
        logging.error(err)
        return

    display_suggestion(suggestion)


if __name__ == '__main__':
    main()
