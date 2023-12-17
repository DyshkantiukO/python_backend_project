from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2


def get_db_connection():
    return psycopg2.connect(host="python_backend_project", database="flaskdb", user="postgres", password="root")


def create_tables():
    commands = (
        """ 
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR (20) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS accounts (
            id SERIAL PRIMARY KEY,
            user_id INT,
            money INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS categories ( 
            id SERIAL PRIMARY KEY, 
            name VARCHAR(20) NOT NULL 
        );

        CREATE TABLE IF NOT EXISTS records ( 
            id SERIAL PRIMARY KEY,
            user_id INT,
            category_id INT, 
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount_of_expenditure FLOAT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        );""")
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import myapplication.views
import myapplication.models
