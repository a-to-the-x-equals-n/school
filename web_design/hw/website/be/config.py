from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


''' FLASK '''

app = Flask(__name__)
CORS(app)


''' SQL ALCHEMY '''

# link flask to sql database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "" # this is the database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Base = declarative_base() # initialize sqlalchemy


''' JAVA WEB TOKENS '''

app.config['JWT_SECRET_KEY'] = "" # this is your public key (if using JWT authentication)
jwt = JWTManager(app)  # initialize JWT


''' BCRYPT '''

bcrypt = Bcrypt(app)