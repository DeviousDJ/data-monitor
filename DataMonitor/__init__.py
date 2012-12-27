#imports
from __future__ import with_statement
from flask import jsonify
from flask import Flask, Response, render_template, request, session, flash, g, redirect, url_for, _app_ctx_stack
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
import pprint
import json
import os
import uuid
import csv
import queries
import pprint
from pymongo import Connection
import re
import time
 
MONGO_CONN = "mongodb://crawler:ondeck1556@jack.mongohq.com:10004/crawler_big"
 
conn = Connection(MONGO_CONN)
db = conn['crawler_big']
 
def get_col_count(col, q=None, n_minutes=5):
	if not q:
		anchor=int(time.time())-60
		q = {"epochstamp": {
		"$gt": anchor-60*n_minutes, 
		"$lt": anchor}}
		print q
	return db[col].find(q).count()
 
def get_collection_counts(n_minutes=5):
    live_collections = [col for col in db.collection_names()
                        if not re.search("system|archive", col)]
    q = {"epochstamp": {"$gt": int(time.time())-60*n_minutes}}
 
    for collection in live_collections:
        yield (collection, get_col_count(collection, q))


# from db import DB

# CONFIG

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# set the secret key.  keep this really secret:
app.secret_key = '1-\xf1\xec\x10\x1eN@Zv\x95\x93\xe3\x0c\x96\xf8H&\xd8\xaa\xdc2\xec\xd9'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	return render_template('home.html')

@app.route('/totaldocs/<colname>')
def total_docs(colname):
	count = db[colname].count()
	for col in db.collection_names():
		if re.search(colname + "_archive", col):
			count += db[col].count()
	return jsonify({
			"collection": colname,
			"count": count
		})

@app.route('/collection_count/<colname>')
def collection_count(colname):
	return jsonify({
			"collection": colname,
			"count": get_col_count(colname, n_minutes=1)
		})


