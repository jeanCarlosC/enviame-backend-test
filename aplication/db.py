from aplication.app import enviroment
from aplication.config import app_config
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

settings = app_config[enviroment]
Session = sessionmaker()
db = SQLAlchemy()
