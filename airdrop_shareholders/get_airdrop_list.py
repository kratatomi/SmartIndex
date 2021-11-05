import json
import pprint  # For printing results in a more readable way

ignored_addresses = ["0xd11bb6a7981780aADc722146a306f7104fD93E9c"]  # Ignoring admin wallet
balance_sheet = {}
decimals = 18 #Decimals of the token
amount_to_share = 1 #Amount of tokens to be airdroppped


def balances(data):
    total_supply = 0
    for block_number in data["blocks"]:
        for txhash in data["blocks"][block_number]:
            for tx in data["blocks"][block_number][txhash]:
                if data["blocks"][block_number][txhash][tx]["from"] == "0x0000000000000000000000000000000000000000":
                    total_supply += data["blocks"][block_number][txhash][tx]["value"] / 10 ** decimals
                if data["blocks"][block_number][txhash][tx]["to"] == "0x0000000000000000000000000000000000000000":
                    total_supply -= data["blocks"][block_number][txhash][tx]["value"] / 10 ** decimals
                if data["blocks"][block_number][txhash][tx]["to"] in balance_sheet:
                    balance_sheet[data["blocks"][block_number][txhash][tx]["to"]] += \
                    data["blocks"][block_number][txhash][tx]["value"] / 10 ** decimals
                if data["blocks"][block_number][txhash][tx]["to"] not in balance_sheet and \
                        data["blocks"][block_number][txhash][tx]["to"] != "0x0000000000000000000000000000000000000000":
                    balance_sheet[data["blocks"][block_number][txhash][tx]["to"]] = \
                    data["blocks"][block_number][txhash][tx]["value"] / 10 ** decimals
                if data["blocks"][block_number][txhash][tx]["from"] in balance_sheet:
                    balance_sheet[data["blocks"][block_number][txhash][tx]["from"]] -= \
                    data["blocks"][block_number][txhash][tx]["value"] / 10 ** decimals
    return total_supply


def airdrop_list(balance_sheet, amount_to_share, total_supply):
    for address in ignored_addresses:
        total_supply -= balance_sheet[address]
        del balance_sheet[address]
    airdrop = {}
    for address in balance_sheet:
        if balance_sheet[address] == 0:
            continue
        airdrop[address] = (balance_sheet[address] / total_supply) * amount_to_share
        print("{} "" {:.8f}".format(address, airdrop[address]))

try:
    file = open("SIDX_events.json", )
    SIDX_data = json.load(file)
    total_supply = balances(SIDX_data)
    airdrop_list(balance_sheet, amount_to_share, total_supply)
except FileNotFoundError:
    print("File with contract events doesn't exist")
