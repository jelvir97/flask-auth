from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db
from forms import RegisterForm, LoginForm

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

@app.route('/register', methods=['POST'])
def handle_user_registration():
    """Validates registration form"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.register(form.username.data,
                                form.password.data,
                                form.email.data,
                                form.first_name.data,
                                form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {user.username}!")
        return redirect("/register")

@app.route('/login', methods=["GET"])
def login():
    """Renders login form for users"""
    form = LoginForm()
    return render_template('login.html',form = form)

@app.route('/login', methods=["POST"])
def handle_user_login():
    """Handles user login form submit"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,form.password.data)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Invalid name/password"]

    return render_template("login.html", form=form)

@app.route('/logout',methods=["POST"])
def logout_user():
    """Removes username from session and returns to login page."""
    session.pop('username')
    return redirect('/login')

@app.route('/secret')
def secret_page():
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')
    
    return 'Secret Pgae'
    

