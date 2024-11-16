#!/usr/bin/env python3

""" Basic Flask app.
Instantiate the Babel object and configure the app to support
multiple languages.
Create a Config class with the following attributes:
    LANGUAGES (list): List of supported languages.
    BABEL_DEFAULT_LOCALE (str): Default language for the app.
    BABEL_DEFAULT_TIMEZONE (str): Default timezone for the app.
Define the route for the root URL.
Create a get_locale function with the babel.localeselector decorator.
Use request.accept_languages to determine the best match
with our supported languages.
"""

from flask import Flask, render_template, request
from flask_babel import Babel

# Initialize the Flask application
app = Flask(__name__)
# Instantiate the Babel object
babel = Babel(app)


# Create the Config class
class Config:
    """
    Configuration class for the application.
        Attributes:
        Languages (list): List of supported languages.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Apply the configuration to the Flask app
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


# Define the route for the root URL
@app.route('/')
def index():
    """Render the index page."""
    return render_template('2-index.html')


# Main entry point of the application
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
