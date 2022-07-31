from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCdtA9S2ufoZeWS9HL7do4mTIlovigUCn8",
  "authDomain": "roei-s-project-e8706.firebaseapp.com",
  "projectId": "roei-s-project-e8706",
  "storageBucket": "roei-s-project-e8706.appspot.com",
  "messagingSenderId": "226041239875",
  "appId": "1:226041239875:web:3e92efb2690df00c9b37f6",
  "measurementId": "G-P3ERC997RB",
  "databaseURL": ""

}

firebase  = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
            error = "Authentication failed"
    return render_template("signin.html")
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add'))
       except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)