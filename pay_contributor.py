import xpring
import requests
import re
import os
from pathlib import Path
import ast

def pay_xrp_testnet(wallet_seed, address, amount):
    # Create a wallet instance using the seed
    wallet = xpring.Wallet.from_seed(wallet_seed)

    # The XRP testnet
    url = 'test.xrp.xpring.io:50051'
    client = xpring.Client.from_url(url)

    # Create a transaction
    txn = client.send(wallet, address, str(amount))

    # Submit txn to the network
    res = client.submit(txn)

    return res

def get_address_from_payid(payid, network, environment):
    # Convert the PayID into a URL e.g.
    # pay$username.github.io -> https://username.github.io/pay
    local_part, domain = payid.split('$')
    url = f'https://{domain}/{local_part}'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    # Look for an address that matches the network
    # and environment we want to use
    for address in data['addresses']:
        if address['paymentNetwork'] == network and \
           address['environment'] == environment:
            return address['addressDetails']['address']

def find_all_payids(msg):
    return re.findall(r'(\S+\$\S+)', msg)

def find_all_variable_names(filename):
    root = ast.parse(filename=filename)
    names = {node.id for node in ast.walk(root) if isinstance(node, ast.Name)}
    return names

def find_all_variable_names_in_dir(path):
    all_names = set()
    filenames = path.glob('**/*.py')
    for filename in filenames:
        all_names |= find_all_variable_names(str(filename))

    return all_names

if __name__ == '__main__':
    old_varnames = find_all_variable_names_in_dir('.old-code')
    new_varnames = find_all_variable_names_in_dir('.new-code')
    print('old', old_varnames)
    print('new', new_varnames)

if __name__ == 'X__main__':

    print("running pay contributor")

    commitmsg = os.environ.get('commitmsg')
    secret = os.environ.get('PAYID_WALLET_SECRET')
    if commitmsg and secret:
        print("commit message:", commitmsg)
        payids = find_all_payids(commitmsg)
        print("Payids found:", payids)

        for payid in payids:
            address = get_address_from_payid(payid, 'XRPL', 'TESTNET')
            if address:
                print(f"Address found for {payid} is {address}")

                amount = 1000000

                pay_xrp_testnet(secret, address, amount)
            else:
                print("No address found for payid:", payid)

    else:
        print("No commit message, nothing to do")