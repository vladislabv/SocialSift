from flask import Flask

app = Flask(__name__)

# Import routes
from gih_site import routes