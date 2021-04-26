"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, redirect, request, session, url_for
from werkzeug.urls import url_parse
from config import Config
from probability import app, db
from probability.forms import LoginForm, ProbabilityForm
from flask_login import current_user, login_user, logout_user, login_required
from probability.models import User
from service import compute_probability
from dto import Person
import msal
import uuid


@app.route('/')
@app.route('/home')
@login_required
def home():
    """Renders home template.

    Returns:
        obj: template
    """
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('index.html', title='Home Page')


@app.route('/probability', methods=['GET', 'POST'])
@login_required
def probability():
    """[summary]

    Returns:
        [type]: [description]
    """
    form = ProbabilityForm(request.form)
    if form.validate_on_submit():
        person1 = Person(form.first_name1, form.last_name1, form.birth_date1, form.bsn1)
        person2 = Person(form.first_name2, form.last_name2, form.birth_date2, form.bsn2)
        
        form.probability = compute_probability(person1, person2)
        return redirect(url_for('home'))
    return render_template('index.html',
                           title='Compute Probability',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    session["state"] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session["state"])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           auth_url=auth_url)


@app.route(Config.REDIRECT_PATH)  
def authorized():
    """Its absolute URL must match your app's redirect_uri set in AAD.

    Returns:
        object: response object (a WSGI application) that, if called,
    redirects the client to the target location
    """
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("home"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        # Acquire a token from a built msal app, along with the appropriate redirect URI
        result = _build_msal_app(
            cache=cache).acquire_token_by_authorization_code(
                request.args["code"],
                scopes=Config.SCOPE,
                redirect_uri=url_for("authorized",
                                     _external=True,
                                     _scheme="https"))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        # Note: In a real app, we'd use the 'name' property from session["user"] below
        # Here, we'll use the admin username for anyone who is authenticated by MS
        user = User.query.filter_by(username="admin").first()
        login_user(user)
        _save_cache(cache)
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    """logs out from web application.

    Returns:
        str: redirect url
    """
    logout_user()
    if session.get("user"):  # Used MS Login
        # Wipe out user and its token cache from session
        session.clear()
        # Also logout from your tenant's web session
        return redirect(Config.AUTHORITY + "/oauth2/v2.0/logout" +
                        "?post_logout_redirect_uri=" +
                        url_for("login", _external=True))

    return redirect(url_for('login'))


def _load_cache():
    """Load the cache from `msal`, if it exists

    Returns:
        TokenCache: token cache.
    """
    cache = msal.SerializableTokenCache()
    if session.get('token_cache'):
        cache.deserialize(session['token_cache'])
    return cache


def _save_cache(cache):
    """Save the cache, if it has changed.

    Args:
        cache (TokenCache): token cache
    """
    if cache.has_state_changed:
        session['token_cache'] = cache.serialize()


def _build_msal_app(cache=None, authority=None):  
    """Returns a ConfidentialClientApplication.

    Args:
        cache (TokenCache, optional): token cache. Defaults to None.
        authority (str, optional): A URL that identifies a token authority. Defaults to None.

    Returns:
        ConfidentialClientApplication: A dict representing the json response from AAD.
    """
    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID,
        authority=authority or Config.AUTHORITY,
        client_credential=Config.CLIENT_SECRET,
        token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    """[Returns the full Auth Request URL with appropriate Redirect URI.

    Args:
        authority (str, optional): A URL that identifies a token authority. Defaults to None.
        scopes (list[str], optional): Scopes requested to access a protected API. Defaults to None.
        state (str, optional): Recommended by OAuth2 for CSRF protection. Defaults to None.

    Returns:
        str: The authorization url.
    """
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True, _scheme="https"))
