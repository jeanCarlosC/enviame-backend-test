#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.enviroment import env
enviroment = env

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from app.config import app_config
from app.db import db
from app.redis import redis


# Import resources


# Flask initialization
app = Flask(__name__)

# CORS enablement
CORS(app)

# Database initialization
db.init_app(app)

# Configuration variables are set according to environment
app.config.from_object(app_config[enviroment])
redis.init_app(app)

#Initialization of api services
api = Api(app)

# Endpoints are defined
@app.route('/', methods=['GET'] )
def welcome():
    return {
        "Status":"OK",
        "message":"Welcome"
    }, 200

# The application starts
app.run(host='0.0.0.0', port=5000, debug=True )
    
        
