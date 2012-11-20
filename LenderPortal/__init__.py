#imports
from __future__ import with_statement
from flask import Flask, render_template, request, session, flash, g, redirect, url_for, _app_ctx_stack
from contextlib import closing
import pprint
import json
import os
import uuid
# from db import DB

# CONFIG

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# set the secret key.  keep this really secret:
app.secret_key = '1-\xf1\xec\x10\x1eN@Zv\x95\x93\xe3\x0c\x96\xf8H&\xd8\xaa\xdc2\xec\xd9'

# mydb = DB()

@app.route('/', methods=['GET', 'POST'])
def dashboard():
	return render_template('home.html')