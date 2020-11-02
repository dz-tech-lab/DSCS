import pandas as pd
import datetime
import mysql.connector
from flask import Flask, render_template, redirect, url_for, flash
# we import the flask_sqlalchemy package
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, PostForm

from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required

app = Flask(__name__)

app.config["SECRET_KEY"] = "enter-a-hard-to-guess-string"

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"
########


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Defining our Classes


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    user_handle = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship("Posts", backref="author", lazy=True)

    def __repr__(self):
        """
        This is the string that is printed out if we call the print function
            on an instance of this object
        """
        return f"User(id: '{self.id}', user_handle: '{self.user_handle}'"


class Posts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # likes = db.relationship("Likes", backref="likes", lazy=True)

    def __repr__(self):
        return f"Posts(id: '{self.id}', content: '{self.content}', author: '{self.user_id}')"


# class Likes(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)


    def __repr__(self):
        return f"Likes(id: '{self.id}', content: '{self.content}', author: '{self.user_id}')"

##############################################
# Routes
##############################################


@ app.route("/")
@login_required
def feed():
    posts = get_tweets()
    posts = posts.sort_values(by=['date_created'], ascending=False)
    query = """
    SELECT *
    FROM User
    LEFT JOIN Posts
    ON User.id == Posts.user_id
    """
    tweet_user = pd.read_sql(query, db.session.bind)
    tweet_user = tweet_user.sort_values(by=['date_created'], ascending=False)
    return render_template("index.html", posts_df=tweet_user)


@ app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("feed"))

    form = RegistrationForm()

    if form.validate_on_submit():
        registration_worked = register_user(form)
        flash("Registration successful")
        if registration_worked:
            flash("Registration successful")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("feed"))

    form = LoginForm()

    if form.validate_on_submit():
        if is_login_successful(form):
            flash("Login successful")
            return redirect(url_for("feed"))
        else:
            if username_wrong(form):
                flash("Username not found")
                return redirect(url_for("register"))
    flash("Wrong Password")
    return render_template("login.html", form=form)


@ app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()

    if form.validate_on_submit():
        add_tweet(form)
        flash("Tweet uploaded successfully")
        return redirect(url_for("feed"))

    flash("Tweet must be less than 140 characters")
    return render_template("tweet.html", form=form)


@app.route("/profile/<user_handle>")
@login_required
def profile(user_handle):
    user = User.query.filter_by(user_handle=user_handle).first()
    first_name = user.first_name
    last_name = user.last_name
    if user is not None:
        return render_template("profile.html", user_handle=user_handle, first_name=first_name,
                               last_name=last_name)
    return redirect(url_for("feed"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

##############################################
# Helper Functions


def register_user(form_data):

    def user_handle_taken(user_handle):
        if User.query.filter_by(user_handle=user_handle).count() > 0:
            return True
        else:
            return False

    if user_handle_taken(form_data.user_handle.data):
        return False

    hashed_password = bcrypt.generate_password_hash(form_data.password.data)

    user = User(first_name=form_data.first_name.data,
                last_name=form_data.last_name.data,
                user_handle=form_data.user_handle.data,
                email=form_data.email.data,
                password=hashed_password)

    db.session.add(user)

    db.session.commit()

    return True


def is_login_successful(form_data):

    user_handle = form_data.user_handle.data
    password = form_data.password.data

    user = User.query.filter_by(user_handle=user_handle).first()

    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return True

    return False


def username_wrong(form_data):
    user_handle = form_data.user_handle.data
    user = User.query.filter_by(user_handle=user_handle).first()

    if user is None:
        return True


def add_tweet(form_data):

    tweet = Posts(content=form_data.content.data,
                  length=len(form_data.content.data),
                  user_id=current_user.id)

    db.session.add(tweet)

    db.session.commit()


def get_tweets():
    posts_df = pd.read_sql(Posts.query.statement, db.session.bind)
    # user_df = pd.read_sql(User.query.statement, db.session.bind)
    return posts_df
#     # and user_df

# def display_profile():
#     pro_df = pd.read_sql(User.query.statement, db.session.bind)
#     return pro_df


if __name__ == "__main__":
    app.run(debug=True)
