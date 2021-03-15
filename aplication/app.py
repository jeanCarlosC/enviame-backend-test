#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from aplication.enviroment import env
enviroment = env

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from aplication.config import app_config
from aplication.db import db
from aplication.redis import redis

# Class utilities
from aplication.helpers.Utilities import Utilities

# Import resources
from aplication.resources.CompanyMaintainer import CompaniesViewResource, CompanyViewResource, CompanyCreateResource, CompanyUpdateResource, CompanyDeleteResource
from aplication.resources.Scripts import loadFakerCompaniesResource, PalindromoScriptResource, EnviameResource


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

# Endpoints company are defined
api.add_resource(CompaniesViewResource, '/companies')
api.add_resource(CompanyViewResource, '/company/<int:_id>')
api.add_resource(CompanyCreateResource, '/company/create')
api.add_resource(CompanyUpdateResource, '/company/update/<int:_id>')
api.add_resource(CompanyDeleteResource, '/company/delete/<int:_id>')

# Endpoints scripts
api.add_resource(loadFakerCompaniesResource, '/scripts/fakeCompanies')
api.add_resource(PalindromoScriptResource, '/scripts/palindrome')
api.add_resource(EnviameResource, '/scripts/createDelivery')

@app.route('/', methods=['GET'] )
def welcome():
    return {
        "Status":"OK",
        "message":"Welcome to python Flask"
    }, 200

# The application starts
app.run(host='0.0.0.0', port=5000, debug=True )
    
        
