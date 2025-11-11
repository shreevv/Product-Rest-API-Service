import os

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "please, tell me... in your heart"
