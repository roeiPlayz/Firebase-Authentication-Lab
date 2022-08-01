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
  "databaseURL": "https://roei-s-project-e8706-default-rtdb.europe-west1.firebasedatabase.app/"

}

firebase  = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


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
            user = {"name" : request.form['Full Name'], "email": request.form['email'], "password": request.form['password'], "bio": request.form['Bio'], "username": request.form['Username']}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    
    if request.method == 'POST':
        try:
            tweet = {"title": request.form['title'], "text": request.form['text'], "uid": login_session['user']['localId']}
            db.child("Tweets").push(tweet)
            return redirect(url_for("/all_tweets"))
        except:
            print("error")
    return render_template("add_tweet.html")


@app.route('/signout', methods = ['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets', methods = ['GET', 'POST'])
def all_tweets():
    return render_template("all_tweets.html", tweet = db.child("Tweets").child().get().val())



if __name__ == '__main__':
    app.run(debug=True)