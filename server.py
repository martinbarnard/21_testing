#!/usr/bin/env python3
# broken test case for logging
# some of these imports are useless, as I'm ripping it out of another app.
from subprocess import call
from uuid import uuid4
from flask import Flask, send_from_directory, session, escape, request
# caching
from flask.ext.cache import Cache

from two1.wallet import Wallet
from two1.bitserv.flask import Payment
from two1.bitrequests import BitTransferRequests

import os
import numpy as np

# configure the app & wallet
app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)
# setup our payback system
transfers=BitTransferRequests(wallet)


# Configure cacheing
# We will need this for the game
cache=Cache(app, config={'CACHE_TYPE':'simple'})

# pulled from os.urandom(24)
def gen_key():
    return os.urandom(24)

# rpi has hardware rng enabled & pointed at /dev/urandom
# this was pulled from it.
# Should we have a secret key generated each time???
app.secret_key=b'\x9e\x98\xe2\t-8\x1a\xda\xc8?\xcf[\x8d\xbe\x10\x81D\xbb\xca\xbd\x01Jd\xeb'

# charge a fixed fee of 100 satoshis per request to the client
# 
payment_amount=100
payout_amount=payment_amount

def cryptorand(n):
    '''
    Pull a random number from /dev/urandom
    we are on a rpi with hardware rng linked to /dev/urandom, so it
    should be good :)
    '''
    a=np.fromstring(os.urandom(n*4), dtype=np.uint32) >> 5
    b = np.fromstring(os.urandom(n*4), dtype=np.uint32) >> 6
    return (a * 67108864.0 + b) / 9007199254740992.0

@app.route('/test')
@payment.required(payment_amount)
def test():
    client_payout_addr = request.args.get('payout_address')
    wallet.send_to(client_payout_addr, payout_amount)
    return "paying you back".format(payout_amount)

@app.errorhandler(500)
def five_hundred(error):
    return escape(error)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=4000)
