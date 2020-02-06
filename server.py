"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)    


@app.route("/users/<int:user_id>")
def user_info(user_id):

    user = User.query.filter_by(user_id=user_id).first()
    return render_template("user_info.html", user=user)


@app.route("/register")
def register_form():

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_process():

    email = request.form.get('username')
    password = request.form.get('password')
    user_email = User.query.filter_by(email=email).first()

    if not user_email:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register_form.html")


@app.route("/login")
def user_login():

    return render_template("login.html")


@app.route("/login", methods=['POST'])
def handle_login():

    username = request.form['username']
    password = request.form['password']
    user_email = User.query.filter_by(email=username).first()

    if password == user_email.password:
        session['current_user'] = username
        flash(f'Logged in as {username}')
        return redirect('/')

    else:
        flash('Wrong password!')
        return redirect('/login')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
