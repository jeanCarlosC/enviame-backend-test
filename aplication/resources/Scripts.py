#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
from flask import Flask, request, jsonify, redirect
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify, render_template, send_from_directory
from datetime import date, datetime
from faker import Faker

from aplication.helpers.Utilities import Utilities

from aplication.models.Company import Company

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
