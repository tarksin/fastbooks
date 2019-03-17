import os
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a26e72f1-d4a7-4ebc-9548-9e8ebb87c049'
    # DATABASE_URL = mysql+pymysql://maxxblog:xynzn987@localhost:3306///maxxblog
    # app.config['
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://maxxblog:xynzn987@localhost:3306/fastbooks'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xynzn987@localhost/fastbooks'

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = DATABASE_URL + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

