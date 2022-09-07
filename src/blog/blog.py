from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app

import requests

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
    try:
        # Checking conditional statement for dev/prod env to determine route to API:
        if app.config["FLASK_ENV"] == 'development':
            
            blog_response = requests.get("http://localhost:8000/blog-api/posts/") 
            category_response = requests.get("http://localhost:8000/blog-api/categories/")
        else:
            blog_response = requests.get("http://rest-api:80/blog-api/posts/")
            category_response = requests.get("http://rest-api:80/blog-api/categories/")

        # If response was successful pass response content to template:
        if blog_response.status_code and category_response.status_code == 200:
        
            categories = category_response.json()
            posts = blog_response.json()

        else:
            categories = []
            posts = []

    except Exception as e:
        categories = []
        posts = []

    return render_template("homepage.html", posts=posts, categories=categories)

# Route for displaying a single blog post:
@blog_bp.route("/post/<blog_id>", methods=["GET"])
def render_blog_post(blog_id: int = None):
    "The method that makes a request to the API for a single blog post and renders it to a template based on its id"
    if blog_id == None:
        return redirect(url_for("homepage"))
    
    # Making API request for single blog post content:
    if app.config["FLASK_ENV"] == 'development':
        response = requests.get(f"http://127.0.0.1:8000/blog-api/posts/{blog_id}")
    else:
        response = requests.get(f"http://rest-api:80/blog-api/posts/{blog_id}")

    if response.status_code == 200:
        # Providing blog content to the template:
        return render_template("render_post.html", post=response.json())


# Route that provides the form for creating a blog post and adding it to the REST API:
@blog_bp.route("/create")
def create_blog_post():
    "Simply renders the blog creation form template"
    return render_template("create_post.html")

# Route that processes the blog form submission by validating and making POST request to the REST API: 
@blog_bp.route("/blog_POST", methods=["POST"])
def make_blog_post_request():
    "The route that actually makes the POST request to the Blog API to create a post"
    # If a username and password are provided make an auth request to the API: 
    username = request.form["username"]
    password = request.form["password"]

    if app.config["FLASK_ENV"] == 'development':
        auth_response = requests.post("http://127.0.0.1:8000/api-token-auth/", data={"username":username, "password":password})
    else: 
        auth_response = requests.post("http://rest-api:80/api-token-auth/", data={"username":username, "password":password}) 
    # If Authentiaction Token is provided by API incorporate it into the blog POST request:
    if auth_response.status_code == 200:

        # Creating Token Authorization header:
        token_auth = f"Token {auth_response.json()['token']}"

        data = {
            "title":request.form["blog_title"],
            "body":request.form["blog_content"],
            "category":request.form["blog_category"],
            "author":request.form["username"]
            }

        # Creating a POST data object from the input form: 
        if app.config["FLASK_ENV"] == "development":

            create_blog_response = requests.post(
                "http://127.0.0.1:8000/blog-api/posts/",
                headers={"Authorization": token_auth},
                data=data
            )

        else:
            create_blog_response = requests.post(
                "http://rest-api:80/blog-api/posts/",
                headers={"Authorization": token_auth},
                data=data
            )

        # If the response was successful, redirecting to now existing blog post: 
        if create_blog_response.status_code == 201:
            return redirect(url_for("blog_bp.render_blog_post", blog_id=create_blog_response.json()["id"]))


    return redirect(url_for("blog_bp.homepage"))
