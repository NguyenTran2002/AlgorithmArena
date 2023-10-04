"""
CODE SOURCE:
https://www.geeksforgeeks.org/how-to-add-authentication-to-your-app-with-flask-login/
"""

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "fbFW24^%572NHWHFfgshfhfcTHshtFVsfg(*&^)"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app) # Flask log in manager that will handle log in and log out requests

# Create user model
class Users(UserMixin, db.Model): # an Users class that's a subclass of UserMixin and db.Model
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

# Initialize app with extension
db.init_app(app)

# Create database within app context
with app.app_context():
	db.create_all() # db.create_all method is used to create the table schema in the database

# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
	
    # If the user made a POST request, create a new user
	if request.method == "POST":
		
        # creates a new Users object with the username and password from the form
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		
        # Add the user to the database
		db.session.add(user)
		
        # Commit the changes made
		db.session.commit()
		
        # Once user account created, redirect them to the login page
		return redirect(url_for("login"))
	
	return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	
    # If a post request was made, find the user by filtering for the username
	if request.method == "POST":
		
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
		
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


# @app.route("/")
# def home():
# 	return render_template("home.html")

@app.route("/")
def home():
    # Retrieve the current user's name from current_user object
    user_name = current_user.username if current_user.is_authenticated else "Guest"
    return render_template("home.html", username=user_name)


if __name__ == "__main__":
	app.run()
