import json
import sys
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request
import ast

# Ganache part
web3 = Web3(HTTPProvider("http://localhost:7545"))

#taking contract instance:
with open('build/contracts/MOSGOVCOVIDQR.json') as f:
    file = json.load(f)

address = file['networks']['5777']['address']
abi = file['abi']
contract = web3.eth.contract(address = address, abi = abi)

#Creating flask App here
app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():

    # print(w3.isConnected())
    return render_template('home.html')

@app.route("/Government", methods=['GET','POST'])
def Government():
    if request.method == 'POST':
        print(web3.isConnected())
        H_name = request.form.get("Hname")
        H_address = request.form.get("Haddr")
        Vacciner = bool(request.form.get("VaccineRespose"))
        price =  request.form.get("price")
        ministry_address = request.form.get("Mname")
        print('''
        {}
        {}
        {}
        {}
        '''.format(type(H_name),type(H_address),type(Vacciner),type(price)))

        try:
            # bid_txn_hash = contract.functions.registerHospital('Hospital_1',hospital_one,'SputnikV',True).transact({'from':ministry_address})
            bid_txn_hash = contract.functions.registerHospital(H_name,H_address,price,Vacciner).transact({'from':ministry_address})
            tx_receipt = web3.eth.waitForTransactionReceipt(bid_txn_hash.hex())
            #print(tx_receipt)
            # logs = manufacturer_contract.events.PillCreated().processReceipt(tx_receipt)
        except ValueError as e:
            message = ast.literal_eval(str(e))['message']
            return render_template('contract_error.html', error=message)

        return render_template('governmentPortal.html')
    else:
        return render_template('governmentPortal.html')

@app.route("/Hospital", methods=['GET','POST'])
def hospital():
    if request.method == 'POST':
        print(web3.isConnected())
        hospital_address = request.form.get("Haddr")
        print(hospital_address)
        try:
            bid_txn_hash = contract.functions.VaccinatePeople().transact({'from':hospital_address})
            tx_receipt = web3.eth.waitForTransactionReceipt(bid_txn_hash.hex())
            #print(tx_receipt)
            # logs = manufacturer_contract.events.PillCreated().processReceipt(tx_receipt)
        except ValueError as e:
            message = ast.literal_eval(str(e))['message']
            return render_template('contract_error.html', error=message)

        return render_template('hospitalPortal.html', name=int(contract.functions.vaccineCard().call())-1)
    else:
        return render_template('hospitalPortal.html')


@app.route("/Verification", methods=['GET','POST'])
def verification():

    if request.method == 'POST':
        print(web3.isConnected())
        certificate_Number = int(request.form.get("certificate_number"))

        try:
            certificate_data = contract.functions.PublicBook(certificate_Number).call()
            if certificate_data[0] == 0:
                reponse_data = "Opps!! Your Vaccine is not registered!"

            else:
                reponse_data = certificate_data
        except ValueError as e:
            message = ast.literal_eval(str(e))['message']
            return render_template('contract_error.html', error=message)

        return render_template('publicPortal.html',certificate_Number = reponse_data)
    else:
        return render_template('publicPortal.html')
    # print(w3.isConnected())


if __name__ == '__main__':
    app.run(debug=True)
