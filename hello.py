#!/usr/bin/python
# encoding=utf8
from flask import Flask, render_template, request, flash, redirect, session, abort
from tinydb import TinyDB,Query
import os
import json
import cPickle as cp
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.secret_key = os.urandom(12)
usersAnnot={"admin":"pwd"}
userAdmin={}
db=""
init = 0
tI = 0
userN = ""


def loadPickle(nameF):
	#a = json.load(open(nameF,"r"))
	#return a["data"]
	return cp.load(open(nameF,"rb"))

rand150 = loadPickle("rand5.cp")
quotes = loadPickle("quotes.cp")


@app.route('/')
def home(user = ""):
	global db, init, tI, userN
	complete = 0
	msg = []
	if user:
		if not init:
			db = TinyDB(user+".json")
			init = 1
		done = []
		for i in db:
			done.append(i["id"])
		toDo = list(set(rand150).difference(done))
		if not toDo:
			complete = 1
		else:
			tI = toDo[0]
			msg = quotes[tI]
	return render_template("index.html", user = user, complete = complete, msg = msg, lenMsg = len(msg))

@app.route('/', methods=['POST'])
def doStuff():
	global db,tI
	tP = {}
	ky = request.form.keys()
	#print ky
	for i in ky:
		if not "other" in i:
			if not request.form[i]:
				tP[i] = request.form['other'+str(i)]
			else:
				tP[i] = request.form[i]
	db.insert({"id":tI,"em":tP})
	return home(user = userN)

@app.route('/login', methods=['POST'])
def do_admin_login():
	global userN
	userN = request.form['username']
	password = request.form['password']
	if userN in usersAnnot:
		if usersAnnot[userN] == password:
			session['logged_in'] = True
		else:
			userN = ""
			flash("Wrong Password Entered.!")
	else:
		flash('User Not Authorized.!')
		userN = ""
	return home(user = userN)

@app.route('/login')
def something():
	return home()

@app.route("/logout")
def logout():
	global userN, db, init, tI
	session['logged_in'] = False
	if db:
		db.close()
	db = ""
	init = 0
	tI = 0
	userN = ""
	return home(user = "")

@app.errorhandler(404)
def page_not_found(e):
	return home()


if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run()