from app import app

# This module exists so that deployment platforms (Railway, Heroku, etc.)
# using the default command `gunicorn main:app` can locate the Flask
# application object without requiring modifications to the Procfile.

if __name__ == "__main__":
    # Allow running locally with ``python main.py`` as well.
    app.run(debug=True)
