import json
import sys
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    # print(w3.isConnected())
    return render_template('base.html')

@app.route("/Government")
def Government():
    # print(w3.isConnected())
    return render_template('governmentPortal.html')

@app.route("/Hospital")
def hospital():
    # print(w3.isConnected())
    return render_template('hospitalPortal.html')

@app.route("/Public")
def public():
    # print(w3.isConnected())
    return render_template('publicPortal.html')

if __name__ == '__main__':
    app.run(debug=True)
