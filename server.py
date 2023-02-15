from flask import *
from db import *


### Auth
import json
from os import environ as env 
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)


@app.before_first_request
def initialie():
    setup() # setup database


@app.route("/")
def home():
    return render_template('base.html') 