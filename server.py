from flask import *
from db import *


### Auth
import json
from os import environ as env 
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth


### Authorization 
from functools import wraps


app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

### Auth Routes
@app.route("/login")
def login():
    # Url to use as the callback
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()

    # This stuff can change
    session["user"] = token
    session["uid"] = token['userinfo']['sid']
    session["email"] = token['userinfo']['email']

    ### images are weird and hosted by google
    ### have to do something other than just img tags
    ### https://stackoverflow.com/questions/40570117/http403-forbidden-error-when-trying-to-load-img-src-with-google-profile-pic
    session["picture"] = token['userinfo']['picture']
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear() # empty the python dictionary
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.before_first_request
def initialie():
    setup() # setup database

@app.route("/")
def home():
    return render_template('base.html') 