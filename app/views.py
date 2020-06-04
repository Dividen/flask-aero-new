import os, logging,random,datetime

# Flask modules
import string

from flask import render_template, request, url_for, redirect, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
from flask_debugtoolbar import DebugToolbarExtension

# App modules
from app import app, lm, db, bc
from app.models import User
from app.forms import LoginForm, RegisterForm, SearchForm

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Passage = Base.classes.Passage
Client = Base.classes.Client


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('layouts/default.html',
                               content=render_template('pages/register.html', form=form, msg=msg))

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)
        email = request.form.get('email', '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'

        else:

            pw_hash = password  # bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'

    else:
        msg = 'Input error'

    return render_template('layouts/default.html',
                           content=render_template('pages/register.html', form=form, msg=msg))


# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    clients = db.session.query(Client).first()
    # cut the page for authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:

            # if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkown user - please register."

    return render_template('layouts/default.html',
                           content=render_template('pages/login.html', form=form, msg=msg,clients=clients),clients=clients)


# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    clients = db.session.query(Client).first()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None
    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template('layouts/default.html',
                               content=render_template('pages/' + path),clients=clients)
    except:

        return render_template('layouts/auth-default.html',
                               content=render_template('pages/404.html'))


# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')


@app.route('/table.html')
def tables():
    clients = db.session.query(Client).first()
    search = SearchForm(request.form)
    passages = db.session.query(Passage).all()
    return render_template('layouts/default.html',
                           content=render_template('pages/table.html', passages=passages, search=search),clients=clients)


@app.route('/table/search', methods=['POST'])
def tablessearch():
    clients = db.session.query(Client).first()
    form = SearchForm(request.form)
    flight=request.form.get("Time")
    date=flight.split('T')[0]
    time=flight.split('T')[1]
    year=int(date.split('-')[0])
    month=int(date.split('-')[1])
    day=int(date.split('-')[2])
    hh=int(time.split(':')[0])
    mm=int(time.split(':')[1])
    if not flight:
        searchdate = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    else:
        searchdate = datetime(year,month,day,hh,mm)

    passages = db.session.query(Passage).filter_by(FlightDate=str(searchdate),OrigCity=form.origcity.data,DestCity=form.destcity.data).all()
    return render_template('layouts/default.html',
                           content=render_template('pages/table.html', passages=passages, search=form,clients=clients),clients=clients)


@app.route('/table1.html')
def tables1():
    clients = db.session.query(Client).all()
    return render_template('layouts/default.html',
                           content=render_template('pages/table1.html', clients=clients),clients=clients)


@app.route('/user.html', methods=["GET"])
def users():
    clients = db.session.query(Client).first()
    values = {9, 4, 5}
    lables = {8, 7, 6}
    pictures = "face-"+str(random.randint(0, 7))+".jpg";
    return render_template('layouts/default.html',
                           content=render_template('pages/user.html', clients=clients, pictures=pictures),clients=clients)

@app.route('/user/drill.html', methods=["GET"])
def users1():
    num = request.args.get("UPK")
    clients = db.session.query(Client).filter_by(UPK=num).first()
    pictures = "face-"+str(random.randint(0, 7))+".jpg";
    return render_template('layouts/default.html',
                          content=render_template('pages/user.html', clients=clients,pictures=pictures),clients=clients)


