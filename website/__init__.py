from flask import Flask

app = Flask(__name__)

# Import routes
from website import routes