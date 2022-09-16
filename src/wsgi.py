from blog import create_app


app = create_app()


if app.config["FLASK_ENV"] == "development":
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8000)
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
"""