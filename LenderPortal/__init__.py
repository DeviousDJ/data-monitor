#imports
from __future__ import with_statement
from flask import Flask, Response, render_template, request, session, flash, g, redirect, url_for, _app_ctx_stack
from contextlib import closing
import pprint
import json
import os
import uuid
import csv
from db import DB
# from db import DB

# CONFIG

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# set the secret key.  keep this really secret:
app.secret_key = '1-\xf1\xec\x10\x1eN@Zv\x95\x93\xe3\x0c\x96\xf8H&\xd8\xaa\xdc2\xec\xd9'

mydb = DB()

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	q = mydb.query("SELECT o.name, o.stagename FROM sf_account a LEFT JOIN sf_opportunity o ON a.id = o.nearest_partner_account__c where a.name = 'Justine PETERSEN' limit 100")
	print q
	return render_template('home.html')

#THIS WORKS
@app.route('/application.csv', methods=['GET', 'POST'])
def generate_large_csv():
    def generate():
        for row in iter_all_rows():
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv')

#THIS SORT OF WORKS
@app.route('/test.csv', methods=['GET', 'POST'])
def generate_large_csv():
	data = 'hello,alfie \nhello,john'
	return Response(data, mimetype='text/csv')