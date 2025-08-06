# Assisted by watsonx Code Assistant 
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route("/hello")
def hello():
    return "Hello, Flask!"

@app.route("/health")
def health():
    """
    Check the health status of the system.

    Returns:
        str: A string indicating the health status, which is "OK" if the system is functioning properly.
    """
    return "OK"


app.run()