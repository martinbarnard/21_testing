#!/usr/bin/env python3
from two1.wallet import Wallet
from two1.bitrequests import BitTransferRequests
import sys

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
requests = BitTransferRequests(wallet)
payout_address=wallet.get_payout_address()

# server address
# TODO: URL from cmdline
port=4000
server_url = 'http://localhost:{}/'.format(port)


def play():
    # get the question from the server
    print("we are sending 100 satoshis and expecting them back")
    url=server_url + 'test?payout_address={}'.format(payout_address)
    res = requests.get(url=url)
    print(res.text)

if __name__ == '__main__':
    play()
