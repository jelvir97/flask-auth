from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
from forms import RegisterForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///auth_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'mangotreeee'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)

@app.route('/')
def home_page():
    """Redirects to /register"""
    return redirect('/register')

@app.route('/register', methods=['GET'])
def register():
    """Renders registration form for new Users"""
    form = RegisterForm()
    return render_template('register.html', form=form)

