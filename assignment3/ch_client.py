from HashRing import ConsistentHashRing
from flask import Flask,json,request, Response
import requests

app = Flask(__name__)

ring = ConsistentHashRing()

list_of_servers = ["192.168.99.100:5001", "192.168.99.100:5002", "192.168.99.100:5003"]

for serverVar in list_of_servers:
    ring[serverVar] = serverVar

#POST requests
for i in range(1, 11):

    requestBody = {
                    "id" : i,
                    "name" : "Foo " + str(i),
                    "email" : "foo" + str(i) + "@bar.com",
                    "category" : "office supplies",
                    "description" : "iPad for office use",
                    "link" : "http://www.apple.com/shop/buy-ipad/ipad-pro",
                    "estimated_costs" : "800",
                    "submit_date" : "12-10-2016"
                    }
    shardKey = requestBody['id']
    url = "http://" + ring[str(shardKey)] + "/v1/expenses"
    data = json.dumps(requestBody)
    response = requests.post(url, data)

#GET requests
for i in range(1, 11):
    expense_id = i
    url = "http://" + ring[str(expense_id)] + "/v1/expenses/" + str(expense_id)
    response = requests.get(url)
    print response.url, response.status_code
    print response.content


'''
@app.route('/v1/expenses/<expense_id>', methods=['GET'])
def retrieveData1(expense_id):

    url = "http://" + ring[str(expense_id)] + "/v1/expenses/" + str(expense_id)
    print url
    response = requests.get(url)
    print response.url, response.status_code
    return Response(response)


@app.route("/v1/expenses", methods=['POST'])
def insertData1():
    # insert new record
    request_data = request.get_json(force=True)

    shardKey = request_data['id']
    url = "http://" + str(ring[shardKey]) + "/v1/expenses"
    data = json.dumps(request_data)
    print url
    response = requests.post(url, data)

    # return the response object
    return Response(response)


if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0", port=8000)

'''
