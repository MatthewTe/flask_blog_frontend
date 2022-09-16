from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import current_app as app
from functools import wraps

import requests

auth_bp = Blueprint(
    "auth_bp",
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Wrapper that checks if a user is "logged in":
def authenticate(f):
    """A functuon wrapper that checks to see if a user session is 'logged in' and contains a token and user. Only let through
    requests that are valid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        # If a session has a user and a token value - let the request go through:
        if "token" and "user" in session:
            pass # Have the API make a request to the API to see if the Token provided is valid.
        else:
            # No user and token value - redirect to login:
            flash("You must be logged in to access this route. Please log in")
            return redirect(url_for("auth_bp.login"))
        
        return f(*args, **kwargs)
    
    return decorated

# Login Route:
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    "Main route that handels the login. Entrypoint for the auth system."

    # If a get request is made, render the login page:
    if request.method == "GET":
        return render_template("login.html")
    else:
        # If a POST request is made - process the login information:
        username = request.form["username"]
        password = request.form["password"]

        # Make autentication request to the API:
        auth_url = f"{app.config['API_URL']}/api-token-auth/"
        api_auth_response = requests.post(auth_url, data={"username":username, "password":password})

        # If authentication is valid - add token and username to user session:
        if api_auth_response.status_code == 200: 
            token = f"Token {api_auth_response.json()['token']}"
            session["user"] = username 
            session["token"] = token

            return redirect(url_for("blog_bp.create_blog_post"))
        
        else:
            # If there was an error with the API response - flash the error and remain on page:
            # Flashing error msg:
            flash(api_auth_response.json()) 
            return render_template("login.html")


# Logout Route:
@auth_bp.route("/logout")
def logout():
    "The basic logout method that clears the session data and redirects to the homepage"
    
    # Removing the user auth if it exists in the session:
    if "token" and "user" in session:
        session.pop("token", None)
        session.pop("user", None)

    # Redirecting to the homepage:
    return redirect(url_for("blog_bp.homepage"))
