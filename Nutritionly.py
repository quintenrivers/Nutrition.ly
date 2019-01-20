import requests
from flask import Flask, request, render_template, jsonify 
import paypalrestsdk
import pyrebase

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyDxsShVirfF3ukNdFN4WDea1woOQ62un5I",
    "authDomain": "nutritionly-9193c.firebaseapp.com",
    "databaseURL": "https://nutritionly-9193c.firebaseio.com",
    "projectId": "nutritionly-9193c",
    "storageBucket": "nutritionly-9193c.appspot.com",
    "messagingSenderId": "336866093958"
}

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AeoEfjH_9XiGmSQluXx34t6SMoOMXczIt9ZZIpLKaFeSAepMgynihbLNlgkIi8iGKHo3moMMM5BS-S4a",
  "client_secret": "EECiI5Aeeca3zaMiV1dUtTRPNl8YT1LZZBvDGVJa-mgoyuRxkST_riZhKX6XjQpL1a4_-g2-q26FnDmg" })

firebase = pyrebase.initialize_app(config)
county = None
donation = 1
db = firebase.database()

#Paypal page will not be home page
@app.route('/')
def index():
	if request.method == 'POST':
		county = request.form['county']	
		donation = request.form['donation']
	return render_template('index.html')

#test
"""
@app.route('/test')
def test():
	print('Ok')
	return render_template('index.html')
"""
	

#creating payment, all info bout payment; before you know who is paying   
@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": county,
                    "sku": "12345", #change if possible
                    "price": donation,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": donation,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)
    
    #returns payment ID
    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
        db.child('Florida').update({county:donation})
    else:
        print(payment.error)

    return jsonify({'success' : success})


if __name__ == "__main__":
	app.run(debug=True)





"""Firebase
 config = {
    apiKey: "AIzaSyDxsShVirfF3ukNdFN4WDea1woOQ62un5I",
    authDomain: "nutritionly-9193c.firebaseapp.com",
    databaseURL: "https://nutritionly-9193c.firebaseio.com",
    projectId: "nutritionly-9193c",
    storageBucket: "nutritionly-9193c.appspot.com",
    messagingSenderId: "336866093958"
  }

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])

def basic():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)
			return render_template('new.html', s=successful)
		except:
			return render_template('new.html', us=unsuccessful)

	return render_template('new.html')

if __name__ == "__main__":
	app.run(debug=True)



@app.route('/tuna')
def tuna():
	return '<h2>Tuna is good</h2>'

#Use <var> to pass in String variables
@app.route('/profile/<username>')
def profile(username):
	return '<h2>Hey there %s</h2>' % username

#Use <data type: var> to pass in all other data types
@app.route('/post/<int:post_id>')
def show_post(post_id):
	return '<h2>Post ID is %s</h2>' % post_id

#returns HTTP request method used
@app.route("/req")
def req():
	return "Method used: %s" % request.method
	

@app.route("/request", methods=['GET', 'POST'])
def request2():
	if request.method == 'POST':
		return "You are using POST"
	else:
		return "You are probably using GET"	
	print("TEST")

#inputs "name" variable into html "template", use {{var}} in html file
@app.route("/intro/<name>")
def intro(name):
	return render_template("profile.html", name=name)

@app.route("/")
@app.route("/<user>")
def index(user=None)
	return render_template("user.html", user=user)
"""


