#imports
from __future__ import with_statement
from flask import Flask, Response, render_template, request, session, flash, g, redirect, url_for, _app_ctx_stack
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from contextlib import closing
import pprint
import json
import os
import uuid
import csv
import queries
import pprint
from db import DB
import users
# from db import DB

# CONFIG

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# set the secret key.  keep this really secret:
app.secret_key = '1-\xf1\xec\x10\x1eN@Zv\x95\x93\xe3\x0c\x96\xf8H&\xd8\xaa\xdc2\xec\xd9'

mydb = DB()

login_manager = LoginManager()

login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
		username = request.form["username"]
		print username
		user = User.query.filter_by(username=username).first()
		print user
		if user:
			remember = request.form.get("remember", "no") == "yes"
			if login_user(USER_NAMES[username], remember=remember):
				flash("Logged in!")
				return redirect(request.args.get("next") or url_for("index"))
			else:
				flash("Sorry, but you could not log in.")
		else:
			flash(u"Invalid username.")
    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	q1 = mydb.query(queries.q1)
	q2 = mydb.query("SELECT COUNT(1) FROM sf_account a LEFT JOIN sf_opportunity o ON a.id = o.nearest_partner_account__c where a.name = 'Justine PETERSEN' limit 100")
	q3 = mydb.query(queries.q3)
	pprint.pprint(q3)
	return render_template('home.html', q1 = q1, q2=q2, q3=q3)

# #THIS WORKS
# @app.route('/application.csv', methods=['GET', 'POST'])
# def generate_large_csv():
#     def generate():
#         for row in iter_all_rows():
#             yield ','.join(row) + '\n'
#     return Response(generate(), mimetype='text/csv')

#THIS SORT OF WORKS
@app.route('/application.csv', methods=['GET', 'POST'])
def generate_large_csv():
	data = mydb.query(queries.q1)
	data = ["|".join(map(str, row)) + "\n" for row in data]
	# csv_data = []
	# for row in data:
	# 	row = [str(item) for item in row]
	# 	row = "|".join(row)
	# 	row += "\n"
	# 	csv_data.append(row)	
	return Response(data, mimetype='text/csv')
