#!/usr/bin/env python3
#
# Item catalog Flask application

from flask import Flask, render_template, request, redirect, url_for
from flask import make_response, jsonify, flash
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import random
import string
import requests
import datetime


app = Flask(__name__)

APP_NAME = "Item Catalog App"


# Connect to Item Catalog DB
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

# Start database session
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


# Create anti-forgery state token - As per in lessons
@app.route('/login')
def showLogin():
    # Create a random 32 sequence of characters as state key
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #TODO: Implement login
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Enable google login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    return None

# User Helper Functions


# Add user based on current session
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
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
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    return None


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
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRestaurants'))


# Home page for Catalog App
@app.route('/')
@app.route('/catalog')
def showAllCategories():
# Display all categories in ascending order
    categories = db_session.query(Category).order_by(asc(Category.title))
    recent_items = db_session.query(CategoryItem).order_by(
                   desc(CategoryItem.last_updated)).limit(7).all()
    return render_template('mainCatalog.html', categories=categories,
                           recent_items=recent_items)


# Display the catalog for a given category
@app.route('/catalog/<category_title>')
def showCategoryCatalog(category_title):
    categories = db_session.query(Category).order_by(asc(Category.title))
    category = db_session.query(Category).filter_by(title=category_title).one()
    items = db_session.query(CategoryItem).filter_by(category_id=category.id)

# TODO: develop catalog template
    return render_template('categoryCatalog.html',
                            categories=categories, items=items, category=category)


# Display the details for a specific item
@app.route('/catalog/<category_title>/<item_title>')
def showItemDetails(category_title, item_title):
    category = db_session.query(Category).filter_by(title=category_title).one()
    item = db_session.query(CategoryItem).filter_by(category_id=category.id,
           title=item_title).one()
    owner = getUserInfo(item.user_id)

    return render_template('itemDetails.html',item=item)


# Edit the details for a specific item
@app.route('/catalog/<item_title>/edit')
def editItem(item):

    return nil


# Delete the details for a specific item
@app.route('/catalog/<item_title>/delete')
def deleteItem(item):

    return nil


# Add a new item
@app.route('/catalog//new_item', methods=['GET', 'POST'])
def newItem():
    #if 'username' not in login_session:
        #return redirect('/login')
    # POST - Create new item and redirect back to the Catalog
    if request.method == 'POST':
        newItem = CategoryItem(
            latest_update=now(),
            title=request.form['title'],
            description= request.form['description'],
            category_id=category.id,
            user_id=login_session['user_id'])
        db_session.add(newItem)
        flash('%s (%s) Successfully Created' % newItem.name, category.title)
        db_session.commit()
        return redirect(url_for('showCategoryCatalog',category))
    # GET - Return form for new item Creation
    else:
        return render_template('newItem.html')


#jsonify support for catalog
@app.route('/catalog.json')
def catelogJSON():
    categories = db_session.query(Category).all()
    catalog = []
    for category in categories:
        items = session.query(CategoryItem).filter_by(
                category_id=category.id).all()
        category.append = ([category.serialize,[item.serialize for item in items]])
    return jsonify(catalog)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
