from client import AvataxClient
from flask import Flask, jsonify, request
import json


client = AvataxClient('fastbooks','1.0','W540','production')
client = client.add_credentials('2000102624','74C6AC3D78E9E859')
# response = client.ping()


app = Flask(__name__)


# print(response.text)
# print(response.json())
# print(response.status_code)
# print(response.raw)

# {"error":{
# "code":"AddressConflictException",
# "message":"You specified both a 'SingleAddress' and a different address type on the element 'transactionModel'.",
# "target":"IncorrectData","details":
#     [
#     {"code":"AddressConflictException","number":301,
#     "message":"You specified both a 'SingleAddress' and a different address type on the element 'transactionModel'.",
#     "description":"When using SingleAddress mode, you may only provide one address element.",
#     "faultCode":"Client",
#     "helpLink":"http://developer.avalara.com/avatax/errors/AddressConflictException","severity":"Error"}]}}


city='Kansas City'
line1="1301 Main St"
region="MO"
postalCode="64101"
amount = 1000

# city='Manhattan'
# line1="301 Bluemont"
# region="KS"
# postalCode=66502
# amount = 555


def getTax(city,line1,postalCode,region,amount):
    tax_document = {
      'addresses': {'SingleLocation': {'city': city,
                                       'country': 'US',
                                       'line1': line1,
                                       'postalCode': postalCode,
                                       'region': region}},
      'commit': False,
      'companyCode': 'DEFAULT',
      'currencyCode': 'USD',
      'customerCode': 'XYZ',
      'date': '2018-10-13',
      'description': 'Silk',

      "lines": [ { "amount": amount } ],

      'purchaseOrderNo': '2018-04-12-001',
      'type': 'SalesInvoice'}



    transaction_response = client.create_transaction(tax_document)
    data = transaction_response.text #json.loads(
# print(transaction_response.text)

    return data
    # print(data)


@app.route('/test12')
def return12():
    return "This returns from /test12"


@app.route('/tax')
def doit():
    tax = getTax(city,line1,postalCode,region,amount)
    tax = '[' + tax + ']'

    tax2 = json.loads(str(tax))
    if tax:
        # print('67 {}'.format(tax2[0]["lines"][0]["id"]))
        for i in range(len(tax2[0]["summary"])):
            print('68 {}:{}'.format(tax2[0]["summary"][i]["jurisName"],tax2[0]["summary"][i]["tax"]      ))
    #    return tax  #  RETURNS JSON-ish (readable with Chrome JSON reader)
        return "Tax amount: {}".format(tax2[0]["totalTax"])
    else:
        return "No joy yet"


app.run()
