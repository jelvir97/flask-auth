from flask import Flask, render_template,flash,get_flashed_messages, request,session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///auth_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'mangotreeee'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)

