import sqlite3
from flask import g
from flask import request
from flask import Markup
from flask import Flask, render_template, session, redirect, url_for, flash, abort
import random
#test
MyApp = Flask(__name__)

MyApp.secret_key = 'myshittylittlesecret'
DATABASE = '/var/www/lab8/shit.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@MyApp.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@MyApp.route("/")
def hello():
  return render_template('shithome.html')

@MyApp.route("/hello")
def hello2():
	var = "<h1>Hello World!</h1>"
        return str(var)

@MyApp.route('/loginval', methods=['POST'])
def loginval():
  password = str(request.form['pass'])
  username = str(request.form['user'])

  user_exists = query_db('SELECT COUNT(*) FROM shitLogin WHERE ShitUser = ?', [username])

  if(user_exists[0][0] == 1):
    password_true = query_db('SELECT COUNT(*) FROM shitLogin WHERE ShitUser = ? AND ShitPass = ?', (username, password))
    if(password_true[0][0] == 1):
      session['loggedin'] = True
      return redirect("/")
    else:
      flash('Invalid Username/Password')
      return redirect("/login")
  else:
      flash('Invalid Username/Password')
      return redirect("/login")

@MyApp.route("/login")
def login():
	return render_template('shitlogin.html')

@MyApp.route("/logout")
def logout():
	session.pop('loggedin', None)
	return redirect("/")

@MyApp.route("/iago", methods=['GET'])
def iago():
  if session.get('loggedin') == True:
    return render_template('shitiago.html')
  else:
    abort(418)

@MyApp.route("/meme", methods=['GET'])
def meme():
  if session.get('loggedin') == True:
    return render_template('dankmemes.html')
  else:
    abort(418)

@MyApp.route("/video")
def video():
  return render_template('shitvideo.html')

if __name__ == "__main__":
        MyApp.run()

@MyApp.route("/guns", methods=['GET'])
def guns():
  if session.get('loggedin') == True:
    return render_template('shitguns.html')
  else:
    abort(418)

@MyApp.errorhandler(418)
def shit418(err):
  return render_template('shit418.html'), 418
    
@MyApp.route('/routes/<var>/<var2>')
def routesFunc(var=None, var2=None):
	return var.upper() + var2
	
@MyApp.route('/reqType', methods=['GET', 'POST'])
def reqType():
	if request.method == 'GET':
		return 'GET'
	if request.method == 'POST':
		return 'POST'

@MyApp.route('/form', methods=['GET'])
def form():
	return render_template('shitinput.html')

@MyApp.route('/submit', methods=['POST'])
def submit():
	return str(len(str(request.form['input'])))

@MyApp.route('/getTest', methods=['GET'])
def getTest():
	return str(request.args.get('key'))


