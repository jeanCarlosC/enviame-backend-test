from app.app import enviroment
from app.config import app_config
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

settings = app_config[enviroment]
Session = sessionmaker()
db = SQLAlchemy()