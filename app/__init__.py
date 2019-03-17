from flask import Flask
from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# "AS WITH OTHER EXTENSIONS, _____ NEEDS TO BE CREATED AND INITIALIZED RIGHT AFTER THE APPLICATION INSTANCE"
#  --Flask Mega-tutorial
# db = SQLAlchemy(app)

#         connection = pymysql.connect(host='localhost', user='maxxblog', password='xnynzn987',
# from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__)
# app.config['DEBUG'] = True      # displays runtime errors in the browser, too
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:xnynzn987@localhost:3306/flicklist'
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = 'a26e72f1-d4a7-4ebc-9548-9e8ebb87c049'
# db = SQLAlchemy(app)


# migrate = Migrate(app, db)
# login_manager = LoginManager(app)

from app import routes, models, maxxDB
