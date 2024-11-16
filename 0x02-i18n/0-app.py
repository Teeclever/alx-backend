#!/usr/bin/env python3

""" Basic Flask app.
"""

from flask import Flask, render_template


# Initialize the Flask application
app = Flask(__name__)

# Define the route for the root URL
@app.route('/')
def index():
    """Render the index page."""
    return render_template('0-index.html')


# Main entry point of the application
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
