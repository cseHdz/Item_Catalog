# Item Catalog App

## Requirements
Interpreter: Python 3

Libraries: flask, sqlalchemy

This project was created using a VirtualBox/Vagrant with Ubuntu 16.04.3 LTS.

## Project Overview
This repository covers the requirements for Udacity - Full Stack Web Development Item Catalog project.

The project creates a Flask application for a Catalog App.
The catalog is comprised of categories and items within such categories.

The app runs by default on [localhost:8000](localhost:8000)

It relies on a SQLLite Database rendered through SQLAlchemy to perform CRUD operations.
It relies on Google Accounts for third-party authentication & authorization services.

The tasks covered by the app are:
1. Display all current categories with the latest added items.
2. Show category specific catalogs with all the items available for that category.
3. Display information for specific items.
4. After logging in, a user has the ability to add, update, or delete item information.
5. Users can only modify those items that they themselves have created.
6. Provides a JSON endpoint for the entire Catalog, Category Specific Catalogs and Individual Items.

## Database Overview
The database consists of 3 classes: User, Category, CategoryItem.
The details of each class can be found on file `database_setup.py`

Category and CategoryItem implement `serialize` to enable jsonify.


## To run this project:
Run the following files with the line `./<file_name>.py` or `python <file_name>.py`
1. Database Setup: Run `database_setup.py`
2. Initialize Database: Run `initialize_data.py`
3. Run the Application: Run `application.py`
