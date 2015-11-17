from flask import Blueprint, session, url_for, request, redirect, flash
from flask_login import login_user
from flask_oauthlib.client import OAuthException
import os

from app import oa, db
from app.models import User, Dictionary
from app.utils import get_or_create

oauth = Blueprint("oauth", __name__)
facebook = oa.remote_app(
    "facebook",
    base_url="https://graph.facebook.com/",
    request_token_url=None,
    access_token_url="/oauth/access_token",
    authorize_url="https://facebook.com/dialog/oauth",
    consumer_key=os.getenv("MYDICTIONARY_FACEBOOK_APP_ID"),
    consumer_secret=os.getenv("MYDICTIONARY_FACEBOOK_APP_SECRET"),
    request_token_params={"scope": "email"}
)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")


@oauth.route("/authorize")
def authorize():
    return facebook.authorize(url_for("oauth.callback", _external=True))


@oauth.route("/callback")
def callback():
    resp = facebook.authorized_response()
    if resp is None:
        flash("Access denied: Reason: %s, error: %s" % (
            request.args["error_reason"], request.args["error_description"]
        ), "error")
    elif isinstance(resp, OAuthException):
        flash("Access denied: %s" % resp.message, "error")

    session["oauth_token"] = (resp["access_token"], "")
    me = facebook.get("/me")
    user, created = get_or_create(User, social_id=me.data.get("id"))
    if created:
        user.name = me.data.get("name")
        dictionary = Dictionary(creator=user)
        db.session.add(user)
        db.session.add(dictionary)
        db.session.commit()

    login_user(user, True)
    return redirect(url_for("main.index"))