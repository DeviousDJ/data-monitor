#imports
from flask import Flask, render_template, request, session, flash
from factual import *
import pprint
import json
import os
import lineOfCredit as LOC

app = Flask(__name__)
app.config.from_envvar('MYAPP_SETTINGS', silent=True)

# set the secret key.  keep this really secret:
app.secret_key = 'WU\xad[\xebo\x12\xc1]UF\x8f\x890S\xaav``>\xf9\xc3v`'

#FACTUAL CONFIG
KEY = 'eN5ZloepyBq1AjB7VDomBZmZpo2NobarjV9WZN2P'
SECRET = '637jGi7GgJQgyQYCPEakrzSTnoSBXA9SjUdedmyc'
factual = Factual(KEY, SECRET)

loc = LOC.LineOfCredit(25000., 0.35)

@app.route('/', methods=['GET'])
def signup():
	print loc
	print 'hello'
	print loc.outstanding_principal
	print loc.available_balance
	return render_template('signup.html')

@app.route('/businessmatch',  methods=['POST'])
def show_business_match():
	#save user input to business session var
	print 'save user input to business session var/n'
	session['business'] = {'name':request.form['name'], 'zip':request.form['zip']}
	print 'save to t/n'
	t = session.get('business')
	print "Company Name in Session: %s" %  t.get('name')
	print "Company Zip in Session: %s" %  t.get('zip')

	#query Factual
	print 'query factual /n'
	table = factual.table('places').filters({"postcode":request.form['zip']})
	q1 = table.search(request.form['name'])
	
	#save Factual results to session var
	print 'factual matches in a session variale: /n'
	session['factual_matches'] = q1.data()[:10]
	m = session.get('factual_matches')
	pprint.pprint(m)

	#return factual matches
	if len(m) == 0: 
		return render_template('business.html')
	else:
		return render_template('businessmatch.html', businesses=m)	

@app.route('/business', methods=['POST', 'GET'])
def show_business():
   	return render_template('business.html')

@app.route('/confirmbusiness', methods=['POST', 'GET'])
def confirm_business():
	print 'just called confirm business \n'
	n = request.form['match_number']
	match=session.get('factual_matches')[0]
	print 'Match: %s' %match
	session['business']['name'] = match.get('name')
	session['business']['phone'] = match.get('tel')
	session['business']['address'] = match.get('address')
	session['business']['city'] = match.get('locality')
	session['business']['state'] = match.get('region')
	session['business']['country'] = match.get('country')
	session['business']['latitude'] = match.get('latitude')
	session['business']['longitude'] = match.get('longitude')
	session['business']['factual_id'] = match.get('factual_id')
	print 'Business: %s \n' % str(session['business'])
	category=match.get('category')
	print 'Category: %s \n' % category
	return render_template('categorymatch.html', category=category)

@app.route('/category', methods=['POST', 'GET'])
def show_category():
	print 'called show category/n'
	return render_template('category.html')

@app.route('/confirmcategory', methods=['POST', 'GET'])
def store_category():
	session['business']['category'] = request.form['category']
	print 'Business: %s \n' % str(session['business'])
	return render_template('owner.html')

@app.route('/owner', methods=['POST', 'GET'])
def show_owner():
	print 'just called show_owner\n'
	return render_template('owner.html')

@app.route('/confirmowner', methods=['POST', 'GET'])
def confirm_owner():
	print 'hello'
	session['owner'] = {'fullname':request.form['fullname'], 'phone':request.form['phone'], 'ssnfour':request.form['ssnfour'], 'dobmonth':request.form['dobmonth'], 'dobday':request.form['dobday'], 'dobyear':request.form['dobyear']}
	print 'hello again'
	print 'Owner: %s \n' %str(session['owner'])
	pprint.pprint(session)
	available_balance = round(loc.available_balance, 2)
	daily_payment = round(loc.daily_payment, 2)
	outstanding_principal=round(loc.outstanding_principal, 2)
	line=loc.line
	return render_template('home.html', line=line, available_balance=available_balance, daily_payment = daily_payment, outstanding_principal=outstanding_principal)

@app.route('/id', methods=['POST', 'GET'])
def show_id():
	return render_template('id.html')

@app.route('/terms', methods=['POST', 'GET'])
def validate_owner():
	session['validate'] = {'userid':'true'}
	return render_template('terms.html')

@app.route('/funding', methods=['POST', 'GET'])
def show_funding():
	return render_template('funding.html')

@app.route('/makedraw', methods=['POST', 'GET'])
def makedraw():
	print 'drawing...'
	loc.draw(5000.)
	flash('You drew $5,000')
	available_balance = round(loc.available_balance, 2)
	daily_payment = round(loc.daily_payment, 2)
	outstanding_principal=round(loc.outstanding_principal, 2)
	line=loc.line
	return render_template('home.html', line=line, available_balance=available_balance, daily_payment = daily_payment, outstanding_principal=outstanding_principal)

@app.route('/makepayment', methods=['POST', 'GET'])
def makepayment():
	print 'one time payment...'
	loc.makePayment(1000.)
	flash('You repaid $1,000')
	available_balance = round(loc.available_balance, 2)
	daily_payment = round(loc.daily_payment, 2)
	outstanding_principal=round(loc.outstanding_principal, 2)
	line=round(loc.line, 2)
	return render_template('home.html', line=line, available_balance=available_balance, daily_payment = daily_payment, outstanding_principal=outstanding_principal)

@app.route('/dailypayment', methods=['POST', 'GET'])
def dailypayment():
	print 'daily payment...'
	loc.makePayment()
	available_balance = round(loc.available_balance, 2)
	daily_payment = round(loc.daily_payment, 2)
	outstanding_principal=round(loc.outstanding_principal, 2)
	line=round(loc.line, 2)
	return render_template('home.html', line=line, available_balance=available_balance, daily_payment = daily_payment, outstanding_principal=outstanding_principal)

if __name__ == '__main__':
    # app.run(debug=True)
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)