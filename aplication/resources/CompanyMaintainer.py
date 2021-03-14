#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import json
from flask import Flask, request, jsonify, redirect
from flask_restful import Resource, reqparse
from aplication import app
from flask import Flask, request, jsonify, render_template, send_from_directory
from datetime import date, datetime

from aplication.helpers.Utilities import Utilities

from aplication.models.Company import Company

class CompaniesViewResource(Resource):
    def get(self):
        data_companies = Company.get_all()
        if data_companies:
            return Utilities.response_services(True,200,"Successful action", data_companies)
        else:
            return Utilities.response_services(False,404,"There are no companies")
class CompanyViewResource(Resource):
    def get(self,_id):
        try:
            data_company = Company.get_data(_id)
            if data_company:
                return Utilities.response_services(True,200,"Successful action", data_company)
            else:
                return Utilities.response_services(False,404,"Company not found")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' line: '+ str(exc_tb.tb_lineno)
            print(msj)
            return Utilities.response_services(False,500,"An unexpected error has occurred", None)
class CompanyCreateResource(Resource):
    required_company_create = {
        "identification":{
            "required":True,
            "type":"str"
        },
        "name":{
            "required":True,
            "type":"str"
        },
        "phone":{
            "required":False,
            "type":"int"
        },
        "mail":{
            "required":False,
            "type":"str",
            "additional_validation":"email"
        }

    }
    def post(self):
        data = request.get_json()
        try:
            validate = Utilities.validateStructureJson(data, CompanyCreateResource.required_company_create)
            if not validate["error"]:
                company_exists = Company.get_data_by_identification(data["identification"])
                if company_exists is None:
                    insert_company = Company.insert_data(data)
                    if insert_company :
                        return Utilities.response_services(True,201,"Company successfully inserted", insert_company)
                    else:
                        return Utilities.response_services(False,500,"An error occurred while inserting the company")
                else:
                    return Utilities.response_services(False,400,"There is already a company with the identification sent")
            else:
                return Utilities.response_services(False,400,validate["message"])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred", None)

class CompanyUpdateResource(Resource):
    required_company_update = {
        "identification":{
            "required":True,
            "type":"str"
        },
        "name":{
            "required":False,
            "type":"str"
        },
        "phone":{
            "required":False,
            "type":"int"
        },
        "mail":{
            "required":False,
            "type":"str",
            "additional_validation":"email"
        }

    }
    def put(self, _id):
        data = request.get_json()
        try:
            validate = Utilities.validateStructureJson(data, CompanyUpdateResource.required_company_update)
            if not validate["error"]:
                company_exists = Company.get_data(_id)
                if company_exists is None:
                    if data["identification"] != company_exists["identification"]:
                        company_identification_exists = Company.get_data_by_identification(data["identification"])
                        if company_identification_exists is not None:
                            return Utilities.response_services(True,400,"There is already a company with the identification sent")
                    update_company = Company.update_data(data)
                    if update_company :
                        return Utilities.response_services(True,204,"Successfully updated company", update_company)
                    else:
                        return Utilities.response_services(False,500,"An error occurred while updating the company")
                else:
                    return Utilities.response_services(False,404,"The company not found")
            else:
                return Utilities.response_services(False,400,validate["message"])
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return Utilities.response_services(False,500,"An unexpected error has occurred", None)

class CompanyDeleteResource(Resource):
    def delete(self, _id):
        company_exists = Company.get_data(_id)
        if company_exists is None:
            return Utilities.response_services(False,404,"The company not found")
        else:
            delete_company = Company.delete_data(_id)
            if delete_company is not None:
                return Utilities.response_services(True,202,"Company successfully eliminated")
            else:
                return Utilities.response_services(True,500,"An error occurred while deleting the company")
