import decimal
import time
import datetime
import base64
import binascii
import requests
import sys
import os
import os.path
import shutil
import re
import string
import random
import json
import math
class Utilities():
    @staticmethod
    def response_services(status, code, message,data = None):
        response = {
            "success": status,
            "message":str(message)
        }
        if data is not None:
            response["data"] = data
        
        return response, code
    
    @staticmethod
    def get_structure(query):
        jsonData = []
        if query:
            """
            This function works only when the query is of type sql 1 model list or sql model (first)
            """
            if isinstance(query, list):
                print("LISTA" + str(len(query)))
                data_response = []
                for table_data in query:
                    d = {}
                    for column in table_data.__table__.columns:
                        data = getattr(table_data, column.name)
                        if isinstance(data, bytes):
                            Bi = binascii.hexlify(data)
                            Bi = str(Bi.decode('ascii'))
                            data = Bi
                        if isinstance(data, datetime.datetime):
                            data = Utilities.dateTimeFormat(data)

                        if isinstance(data, datetime.date):
                            data = Utilities.dateFormat(data)

                        d[column.name] = data
                    if len(query) > 1:
                        data_response.append(d)
                    else:
                        data_response = d
            else:
                print("OTRO")
                d = {}
                for column in query.__table__.columns:
                    data = getattr(query, column.name)
                    if isinstance(data, bytes):
                        Bi = binascii.hexlify(data)
                        Bi = str(Bi.decode('ascii'))
                        data = Bi
                    if isinstance(data, datetime.datetime):
                        data = Utilities.dateTimeFormat(data)
                    if isinstance(data, datetime.date):
                            data = Utilities.dateFormat(data)
                    d[column.name] = data
                if len(query) > 1:
                    data_response.append(d)
                else:
                    data_response = d
        return  data_response
    
    @staticmethod
    def get_structure_collection(query):
        """
            This function works only when the query is of type select all()
        """
        first = False
        name_first_table = ""
        json_primary = {}
        primary_key = None
        foreign_key = None
        if query:
            for tables in query:
                for data_table in tables:
                    if data_table:
                        current_table = str(data_table.__table__)
                        if not first:
                            name_first_table = current_table
                            first = True

                        col = {}
                        for column in data_table.__table__.columns:
                            data = getattr(data_table, column.name)

                            if isinstance(data, bytes):
                                Bi = binascii.hexlify(data)
                                Bi = str(Bi.decode('ascii'))
                                data = Bi
                                #data = data.decode("ISO-8859-1")
                            if isinstance(data, datetime.datetime):
                                data = Utilities.dateTimeFormat(data)
                                
                            if isinstance(data, datetime.date):
                                data = Utilities.dateFormat(data)
                            col[column.name] = data

                        if name_first_table == current_table:
                            primary_key = int(getattr(data_table, "id"))
                            if not primary_key in json_primary:
                                
                                json_primary[primary_key] = {}
                                json_primary[primary_key] = col
                        else:
                            foreign_key = int(getattr(data_table, "id"))
                            if not current_table in json_primary[primary_key]:
                                json_primary[primary_key][current_table] = {}
                                if not foreign_key in json_primary[primary_key][current_table]:
                                    json_primary[primary_key][current_table][foreign_key] = {}
                                    json_primary[primary_key][current_table][foreign_key] = col
                                else:
                                    json_primary[primary_key][current_table][foreign_key] = col
                            else:
                                if not foreign_key in json_primary[primary_key][current_table]:
                                    json_primary[primary_key][current_table][foreign_key] = {}
                                    json_primary[primary_key][current_table][foreign_key] = col
                                else:
                                    json_primary[primary_key][current_table][foreign_key] = col
        return  json_primary
    
    @staticmethod
    def dateFormat(fecha):
    	dia = str(fecha.day)
    	dia = "0"+dia if len(dia) == 1 else dia
    	mes = str(fecha.month)
    	mes = "0"+mes if len(mes) == 1 else mes
    	anio = str(fecha.year)

    	fechaFormateada =  dia + "-" + mes + "-" + anio
    	return fechaFormateada
    
    @staticmethod
    def dateTimeFormat(fecha):
    	return str(fecha.strftime("%d-%m-%Y %H:%M"))

    @staticmethod
    def validateEmail(email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex,email)):  
            ResponseBool = True
        else:  
            ResponseBool = False
        return ResponseBool 
    
    @staticmethod
    def validateStructureJson(data, jsonRequired):
        types = {
            "str":str,
            "int":int
        }
        error = False
        message = ""
        try:
            if data is not None:
                for attribute in jsonRequired:
                    if (attribute not in data or data[attribute] == None or data[attribute] == "") and jsonRequired[attribute]["required"]:
                        message = attribute + " is required "
                        error = True
                        break
                    elif attribute in data and not isinstance(data[attribute],types[jsonRequired[attribute]["type"]]):
                        message = attribute + " the data type is wrong, correct is " + jsonRequired[attribute]["type"]
                        error = True
                        break
                    elif attribute in data and "additional_validation" in jsonRequired[attribute]:
                        if jsonRequired[attribute]["additional_validation"] == "email":
                            if not Utilities.validateEmail(data[attribute]):
                                message = "Invalid email"
                                error = True
                                break
            else:
                message = "A data json is required"
                error = True

            return {"error":error, "message":message}
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return {"error":True, "message":"An unexpected error has occurred"}