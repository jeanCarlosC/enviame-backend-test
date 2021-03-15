#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
from random import randint
from flask import Flask, request, jsonify, redirect
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify, render_template, send_from_directory
from datetime import date, datetime
from faker import Faker
from aplication.app import app_config, enviroment

from aplication.helpers.Utilities import Utilities

from aplication.models.Company import Company
from aplication.models.LogsEnviame import LogsEnviame

class loadFakerCompaniesResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quantity',
            type=int,
            required=True,
            help="You must indicate an quantity"
        )
        params = parser.parse_args()
        try:
            fake = Faker()
            data_response = []
            error_response = []
            for item in range(params["quantity"]):
                data = {
                    "identification": fake.bothify(text='#########'),
                    "name": fake.company(),
                    "address": fake.address(),
                    "status": 1,
                    "phone": fake.bothify(text='2########'),
                    "mail": fake.company_email()
                }
                data_company = Company.insert_data(data)
                if data_company is not None:
                    data_response.append(data_company)
                else:
                    error_response.append(data)
            if len(error_response) == 0:
                return Utilities.response_services(True,201,"Companies successfully inserted",data_response)
            else:
                return Utilities.response_services(True,201,"Some inserts with errors")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred")

class PalindromoScriptResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('string',
            type=str,
            required=False
        )
        params = parser.parse_args()
        try:
            string = "afoolishconsistencyisthehobgoblinoflittlemindsadoredbylittlestatesmenandphilosophersanddivineswithconsistencyagreatsoulhassimplynothingtodohemayaswellconcernhimselfwithhisshadowonthewallspeakwhatyouthinknowinhardwordsandtomorrowspeakwhattomorrowthinksinhardwordsagainthoughitcontradicteverythingyousaidtodayahsoyoushallbesuretobemisunderstoodisitsobadthentobemisunderstoodpythagoraswasmisunderstoodandsocratesandjesusandlutherandcopernicusandgalileoandnewtonandeverypureandwisespiritthatevertookfleshtobegreatistobemisunderstood" if params["string"] is None else params["string"]
            return Utilities.getPalindromesFromString(string)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred")

class EnviameResource(Resource):
    def post(self):
        try:
            payload = Utilities.get_json_create_delivery()
            url = app_config[enviroment].URLS_ENVIAME["create_delivery"]
            print(url)
            headers = {'Accept':'application/json', 'Content-Type':'application/json', 'api-key':'ea670047974b650bbcba5dd759baf1ed'}
            data_inser_log = {
                'name':'create_delivery',
                'status':0,
                'payload':json.dumps({
                    'headers':headers,
                    'payload':payload
                })
            }
            data_insert = LogsEnviame.insert_data(data_inser_log)
            r = requests.post(url, data = json.dumps(payload), headers= headers)
            if r.status_code == 201:
                rs = json.loads(r.text)
                data_update_log = {
                    'response':json.dumps(rs),
                    'status':1
                }
                data_update = LogsEnviame.update_data(data_insert['id'],data_update_log)
                return Utilities.response_services(True,201,"Delivery created successfully",data_update)
            else:
                rs = json.loads(r.text)
                data_update_log = {
                    'response':json.dumps(rs),
                    'status':2
                }
                data_update = LogsEnviame.update_data(data_insert['id'],data_update_log)
                return Utilities.response_services(False,500,"An error occurred while inserting the delivery")
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred")

class DeliveryTimeCalculationResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('km',
            type=int,
            required=False
        )
        params = parser.parse_args()
        try:
            km = randint(0, 2000) if params["km"] is None else params["km"]
            days = Utilities.fibonacciDelivery(km)
            message = "time for delivery for a distance of "+str(km)+" km is " + str(days) + " days"
            return Utilities.response_services(True,200,message)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred")
class FibonacciDivisorsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('divisors',
            type=int,
            required=False
        )
        params = parser.parse_args()
        try:
            limit_divisors = 1000 if params["divisors"] is None else params["divisors"]
            return Utilities.response_services(True,200,"The first number in the fibonacci sequence with more than "+str(limit_divisors)+" divisors is : "+str(Utilities.fibonacciDivisors(limit_divisors)))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred")