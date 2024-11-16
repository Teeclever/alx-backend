#!/usr/bin/env python3

""" Basic Flask app with mocked user login system and timezone support.
Instantiate the Babel object and configure the app to support multiple languages.
Create a Config class with the following attributes:
    LANGUAGES (list): List of supported languages.
    BABEL_DEFAULT_LOCALE (str): Default language for the app.
    BABEL_DEFAULT_TIMEZONE (str): Default timezone for the app.
Define the route for the root URL.
Create a get_locale function with the babel.localeselector decorator.
Use request.accept_languages to determine the best match with our supported languages.
Implement a mocked user login system.
Add timezone support with get_timezone function.
"""

from flask import (
    Flask,
    render_template,
    request,
    g
)
from flask_babel import Babel
import pytz


# Initialize the Flask application
app = Flask(__name__)
# Instantiate the Babel object
babel = Babel(app)


# Create the Config class
class Config:
    """
    Configuration class for the application.
    Attributes:
        LANGUAGES (list): List of supported languages.
        BABEL_DEFAULT_LOCALE (str): Default language for the app.
        BABEL_DEFAULT_TIMEZONE (str): Default timezone for the app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Apply the configuration to the Flask app
app.config.from_object(Config)

# User table to mock a database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """_summary_
    Returns:
        _type_: _description_
    """
    id = request.args.get('login_as')
    if id is not None and int(id) in users.keys():
        return users.get(int(id))
    return None


@app.before_request
def before_request():
    """Execute before each request to retrieve user information.
    Retreives the user and assigns it to the global variable g.user.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    locale_url = request.args.get('locale')
    user_settings_locale = g.user.get('locale')
    locale_header = request.headers.get('Accept-Language')

    if locale_url in app.config['LANGUAGES']:
        return locale_url
    if (g.user and user_settings_locale in app.config['LANGUAGES']):
        return user_settings_locale
    if (locale_header and locale_header in app.config['LANGUAGES']):
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    return app.config['LANGUAGES'][0]


@babel.timezoneselector
def get_timezone():
    """Determine the best match for supported timezones."""
    url_timezone = request.args.get('timezone')
    try:
        tz = pytz.timezone(url_timezone)
        return tz
    except pytz.UnknownTimeZoneError:
        tz = app.config['BABEL_DEFAULT_TIMEZONE']

    try:
        usr_tz = g.user.get('timezone')
        tz = pytz.timezone(usr_tz)
        return tz
    except pytz.UnknownTimeZoneError:
        tz = app.config['BABEL_DEFAULT_TIMEZONE']


babel.init_app(app)  # No 'localeselector' attribute here


# Define the route for the root URL
@app.route('/', strict_slashes=False)
def index() -> str:
    """Render the index page."""
    return render_template('7-index.html')


# Main entry point of the application
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(port="5000", host="0.0.0.0", debug=True)
