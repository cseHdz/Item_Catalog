#!/usr/bin/env python3
#
# Item catalog Flask application

from flask import Flask, render_template, request, redirect, url_for
from flask import make_response, jsonify, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from Item_Catalog.database_setup import Base, Category, CategoryItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import random
import string
import requests
import datetime
import time
import psycopg2
import os

app = Flask(__name__)

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# Connect to Item Catalog DB
engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

secrets = os.path.join(PROJECT_ROOT, 'client_secrets.json')
CLIENT_ID = json.loads(open(secrets, 'r').read())['web']['client_id']

APP_NAME = "Item Catalog App"

Base.metadata.bind = engine

# Start database session
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


# Enable google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(secrets, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    return output

# User Helper Functions


# Add user based on current session
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# Retrieve a user record from db if user_id exists
def getUserInfo(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


# Retrieve a user record from db if email found
def getUserID(email):
    user = db_session.query(User).filter_by(email=email).scalar()
    if (user):
        return user.id
    else:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                   'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showAllCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showAllCategories'))


# Home page for Catalog App
@app.route('/')
@app.route('/catalog')
def showAllCategories():
    # Display all categories in ascending order
    categories = db_session.query(Category).order_by(asc(Category.title))
    recent_items = db_session.query(CategoryItem).order_by(
                   desc(CategoryItem.last_updated)).limit(7).all()
    return render_template('mainCatalog.html',
                           categories=categories,
                           recent_items=recent_items)


# Display the catalog for a given category
@app.route('/catalog/<category_title>')
def showCategoryCatalog(category_title):
    categories = db_session.query(Category).order_by(asc(Category.title))
    category = db_session.query(Category).filter_by(title=category_title).one()
    items = db_session.query(CategoryItem).filter_by(
            category_id=category.id).order_by(asc(CategoryItem.title))
    return render_template('categoryCatalog.html',
                           categories=categories,
                           items=items, category=category)


# Display the details for a specific item
@app.route('/catalog/<category_title>/<item_title>')
def showItemDetails(category_title, item_title):
    category = db_session.query(Category).filter_by(title=category_title).one()
    item = db_session.query(CategoryItem).filter_by(category_id=category.id,
                                                    title=item_title).one()
    if 'username' not in login_session or\
       item.user_id != login_session['user_id']:
        return render_template('itemDetails_public.html', item=item)
    else:
        return render_template('itemDetails.html', item=item)


# Edit a Category Item
@app.route('/catalog/<item_title>/edit', methods=['GET', 'POST'])
def editItem(item_title):
    if 'username' not in login_session:
        return redirect(url_for('showAllCategories'))
    editedItem = db_session.query(CategoryItem).filter_by(
                 title=item_title).one()
    if editedItem.user_id != login_session['user_id']:
        redirect(url_for('showItemDetails', item_title,
                        itemToDelete.category_name))
    if request.method == 'POST':
        if request.form['item_title']:
            editedItem.title = request.form['item_title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category_title'] != editedItem.category_name:
            newCategory = db_session.query(Category).filter_by(
                          title=request.form['category_title']).one()
            editedItem.category_id = newCategory.id
            editItem.category = newCategory
        db_session.add(editedItem)
        db_session.commit()
        flash('%s Successfully Edited' % editedItem.title)
        return redirect(url_for("showItemDetails",
                        category_title=editedItem.category_name,
                        item_title=editedItem.title))
    else:
        categories = db_session.query(Category).order_by(asc(Category.title))
        return render_template('editCategoryItem.html',
                               item=editedItem,
                               categories=categories)


# Edit a Category Item
@app.route('/catalog/<item_title>/delete', methods=['GET', 'POST'])
def deleteItem(item_title):
    if 'username' not in login_session:
        return redirect(url_for('showAllCategories'))
    itemToDelete = db_session.query(CategoryItem).filter_by(
                   title=item_title).one()
    if itemToDelete.user_id != login_session['user_id']:
        redirect(url_for('showItemDetails', item_title,
                        itemToDelete.category_name))
    if request.method == 'POST':
        db_session.delete(itemToDelete)
        db_session.commit()
        flash('%s Successfully Deleted' % itemToDelete.title)
        return redirect(url_for('showAllCategories'))
    else:
        categories = db_session.query(Category).order_by(asc(Category.title))
        return render_template('deleteCategoryItem.html',
                               item=itemToDelete,
                               categories=categories)


# Create a new Category Item
@app.route('/catalog/newItem', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect(url_for('showAllCategories'))
    # POST - Create new item and redirect back to the Catalog
    if request.method == 'POST':
        item = db_session.query(CategoryItem).filter_by(
               title=request.form['item_title']).scalar()
        if (item):
            return """<script>function myFunction() {
                        alert('Name already taken. Please select a new name.');
                        window.history.back();}
                    </script><body onload='myFunction()'>"""
        else:
            category = db_session.query(Category).filter_by(
                       title=request.form['category_title']).one()
            newItem = CategoryItem(last_updated=datetime.datetime.now(),
                                   title=request.form['item_title'],
                                   description=request.form['description'],
                                   category_id=category.id,
                                   user_id=login_session['user_id'])
            db_session.add(newItem)
            db_session.commit()
            return redirect(url_for('showAllCategories'))
    # GET - Return form for new item Creation
    else:
        categories = db_session.query(Category).order_by(asc(Category.title))
        return render_template('newCategoryItem.html', categories=categories)


# JSON Support
@app.route('/catalog/JSON')
def catalogJSON():
    categories = db_session.query(Category).all()
    catalog = {'Category': [category.serialize for category in categories]}
    return jsonify(catalog)


# JSON support for categories
@app.route('/catalog/<category_title>/JSON')
def categoryJSON(category_title):
    category = db_session.query(Category).filter_by(title=category_title).one()
    return jsonify(category.serialize)


# JSON support for individual items
@app.route('/catalog/<category_title>/<item_title>/JSON')
def itemJSON(category_title, item_title):
    category = db_session.query(Category).filter_by(title=category_title).one()
    item = db_session.query(CategoryItem).filter_by(category_id=category.id,
                                                    title=item_title).one()
    return jsonify(item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run()
