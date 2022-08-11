# Dependency
from flask import Flask

# Create a new flask.
app = Flask(__name__)

# Define root of the first route.
@app.route('/')
def hello_world():
    return 'Hello World'
