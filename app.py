from flask import Flask, render_template,flash,get_flashed_messages, request,session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db, Feedback
from forms import RegisterForm, LoginForm, AddFeedbackForm, UpdateFeedbackForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///auth_demo'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = 'mangotreeee'
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)

@app.route('/')
def home_page():
    """Redirects to /register"""
    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    return redirect('/register')

@app.route('/register', methods=['GET'])
def register():
    """Renders registration form for new Users"""
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
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
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
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
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid name/password"]

    return render_template("login.html", form=form)

@app.route('/logout')
def logout_user():
    """Removes username from session and returns to login page."""
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>')
def user_info(username):
    """Renders page with user info and feedback."""
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()
    posts = Feedback.query.filter_by(username=username).all()
    
    return render_template('user_info.html',user=user, posts=posts)

@app.route('/users/<username>/feedback/add')
def add_feedback_form(username):
    """renders form for adding new feedback"""
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')
    if username == session['username']:
        user = User.query.filter_by(username=username).first()
        form = AddFeedbackForm(username=username)

        return render_template('feedback_form.html',user = user, form=form)
    
    return redirect(f'/users/{session["username"]}')

@app.route('/users/<username>/feedback/add', methods=['POST'])
def handle_feedback_form_post(username):
    """Handles adding feedback request."""
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')
    form = AddFeedbackForm()
    if username == session['username'] and form.validate_on_submit():
        fb = Feedback(title=form.title.data,content=form.content.data,username=form.username.data)
        db.session.add(fb)
        db.session.commit()
        return redirect(f'/users/{username}')
    return redirect(f'/users/{username}/feedback/add')
    
@app.route('/feedback/<id>/delete', methods=["POST"])
def delete_feedback(id):
    """Deletes feedback from db."""
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')
    
    fb= Feedback.query.filter_by(id=id).one()

    if session['username'] == fb.username:
        db.session.delete(fb)
        db.session.commit()
        flash('Success! Feedback deleted.')
    else:
        flash('You do not have permission to delete that feedback.')
    return redirect(f"/users/{session['username']}")

@app.route('/feedback/<id>/update')
def render_feedback_update_form(id):
    """Renders form for updating feedback."""
    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')

    fb = Feedback.query.filter_by(id=id).one()
    
    if fb.username == session['username']:

        form = UpdateFeedbackForm(title=fb.title,content=fb.content)
        return render_template('update_feedback.html',form=form,fb=fb)

@app.route('/feedback/<id>/update',methods=['POST'])
def handle_feedback_update(id):
    """Updates feedback and adds changed to db. Redirects to user info page."""

    if "username" not in session:
        flash('You must be signed in to view this page.')
        return redirect('/login')

    fb = Feedback.query.filter_by(id=id).one()

    if fb.username == session['username']:
        form = UpdateFeedbackForm()
        fb.title = form.title.data
        fb.content = form.content.data
        db.session.commit()

    return redirect(f'/users/{session["username"]}')