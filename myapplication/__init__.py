from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_restful import Api
from flask_jwt_extended import JWTManager
import psycopg2


def get_db_connection():
    return psycopg2.connect(host="dpg-clvkga6d3nmc738e26ag-a", database="flaskdb_7uea", user="admin", password="yZqV5iPhvzOI9gPEVWVOfpV2zGm0DMXJ")


def create_tables():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""ALTER TABLE users
        ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT 'default_password';""")
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ALGORITHM'] = "HS256"
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
create_tables()

import myapplication.views
import myapplication.models
