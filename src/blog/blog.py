from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import current_app as app

import requests

# Importing auth decorators:
from .auth.auth_routes import authenticate

# Blog Blueprint:
blog_bp = Blueprint(
    "blog_bp",
    __name__,
    template_folder='templates',
    static_folder='static'
)

# Main homepage route:
@blog_bp.route("/", methods=["GET"])
def homepage():
    "Render homepage with blog posts recieved from the API"
    
    # Make request to the Blog Post API and Blog Category API:
    # Building URLS:
    blog_url = f"{app.config['API_URL']}/blog-api/posts/"
    category_url = f"{app.config['API_URL']}/blog-api/categories/"
    
    blog_response = requests.get(blog_url)
    category_response = requests.get(category_url)
    
    # If response was successful pass response content to template:
    if blog_response.status_code and category_response.status_code == 200:
        posts = blog_response.json()
        categories = category_response.json()
    
    # If the response was unsucessful, pass an empty list to the template and flash the error:
    else:
        posts = []
        categories = []
        flash(blog_response.json())
        flash(category_response.json())

    return render_template("homepage.html", posts=posts, categories=categories)

# Route for displaying a single blog post:
@blog_bp.route("/post/<blog_id>", methods=["GET"])
def render_blog_post(blog_id: int = None):
    "The method that makes a request to the API for a single blog post and renders it to a template based on its id"
    if blog_id == None:
        return redirect(url_for("homepage"))
    
    # Making API request for single blog post content:
    # Building specific blog based on id:
    blog_id_url = f"{app.config['API_URL']}/blog-api/posts/{blog_id}"
    blog_id_response = requests.get(blog_id_url) 

    if blog_id_response.status_code == 200:
        # Providing blog content to the template:
        return render_template("render_post.html", post=blog_id_response.json())


# Route that provides the form for creating a blog post and adding it to the REST API:
@blog_bp.route("/create", methods=["GET", "POST"])
@authenticate
def create_blog_post():
    """If a get request is made, renders the blog creation form template. If a post request is made,
    makes a POST request to the API to create a blog post with form content.
    """
    if request.method == "GET":
        return render_template("create_post.html")
    
    # Blog post creation logic:
    else:
        # Extracting token from user session:
        token = session["token"]

        # Creating payload from forms:
        data = {
            "title":request.form["blog_title"],
            "body":request.form["blog_content"],
            "category":request.form["blog_category"],
            "author":session["user"]
        }

        # Making POST request to the API to create blog post:
        blog_creation_endpoint = f"{app.config['API_URL']}/blog-api/posts/"
        API_response = requests.post(blog_creation_endpoint, data=data, headers={"Authorization": token})

        # If the response was successful, redirecting to now existing blog post: 
        if API_response.status_code == 201:
            return redirect(url_for("blog_bp.render_blog_post", blog_id=API_response.json()["id"]))
        else:
            # If it was not sucessful stay on blog creation page and flash error:
            flash(API_response.json())
            return render_template("create_post.html")

