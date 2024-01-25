from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# Note that the getenv() function is part of Python's built-in os module.
# But because we used a .env file to fake the environment variable,
# we need to first call load_dotenv() from the python-dotenv module.
# In production, DB_URL will be a proper environment variable.
# connect to database using env variable, The engine variable manages the overall connection to the database.
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
Session = sessionmaker(bind=engine)  # The Session variable generates temporary connections for (CRUD) operations.
Base = declarative_base()  # The Base class variable helps us map the models to real MySQL tables.
# Use 'python app/db/__init__.py'  to run and test the connection:
# Test if the connection was successful
if __name__ == "__main__":
    try:
        # Attempt to connect to the database
        connection = engine.connect()
        print(f"Successfully connected to {getenv('DB_URL')}!")
    except Exception as e:
        print(f"An error occurred: {e}")


def init_db(app):
    Base.metadata.create_all(engine)  # We're using the same Base.metadata.create_all() method from the seeds.py file

    app.teardown_appcontext(close_db)  # Flask will run close_db() together this built-in teardown_appcontext() method.


def get_db():
    if 'db' not in g:  # if db is not in the context
        g.db = Session()  # store db connection in app context

    return g.db  # Whenever this function is called, it returns a new session-connection object


# Session directly from the db package, but using a function
# means that we can perform additional logic before creating the database connection.
# For instance, if get_db() is called twice in the same route,
# we won't want to create a second connection. Rather, it will make more sense to return the existing connection
# But how will we know if a connection has already been created per route?
# Implement Application Context in Flask
# This is where the Flask application context helps.
# Flask creates a new context every time a server request is made.
# When the request ends, the context is removed from the app.
# These temporary contexts provide global variables, like the g object,
# that can be shared across modules as long as the context is still active.

# Adding a close function to the app context, to close the db after the queries terminate
def close_db(e=None):
    db = g.pop('db', None)  # The pop() method attempts to find and remove db from the g object.
    # If db exists (that is, db doesn't equal None), then db.close() will end the connection.

    if db is not None:
        db.close()
# pop() method attempts to find and remove db from the g object.
# If db exists (that is, db doesn't equal None), then db.close() will end the connection.
# The close_db() function won't run automatically, though.
# We need to tell Flask to run it whenever a context is destroyed.

# Heroku Deploying with python
# Recall that SQLAlchemy needs to be paired with a connector so that it knows the type of
# SQL database that it's working with. The connector that you installed earlier is called pymysql.
# To use it, you need to reference it in the database connection URL.
#
# In the Heroku dashboard, create a new environment variable called DB_URL. Copy the JAWSDB_URL value,
# then paste it into the value field for DB_URL. Change the value to mysql+pymysql:// to include the connector.
# Then click "Add" to set the variable.
