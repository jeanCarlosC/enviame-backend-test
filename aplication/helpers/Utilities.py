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
from functools import reduce
from math import sqrt

from aplication.app import app_config, enviroment

class Utilities():
    @staticmethod
    def response_services(status, code, message,data = None):
        try:
            response = {
                "success": status,
                "message":str(message)
            }
            if data is not None:
                response["data"] = data
            
            return response, code
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msj = 'Error: '+ str(exc_obj) + ' File: ' + fname +' linea: '+ str(exc_tb.tb_lineno)
            print(str(msj))
            return {"success":False, "message":"An unexpected error has occurred"} , 500
    
    @staticmethod
    def get_structure(query):
        jsonData = []
        if query:
            """
            This function works only when the query is of type sql 1 model list or sql model (first)
            """
            data_response = []
            if isinstance(query, list):
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
                if isinstance(query, list) and len(query) > 1:
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
    
    @staticmethod
    def getPalindromesFromString(s):
        m = dict() 
        n = len(s) 
    
        # table for storing results (2 rows for odd- 
        # and even-length palindromes 
        R = [[0 for x in range(n+1)] for x in range(2)] 
        # Find all sub-string palindromes from the given input 
        # string insert 'guards' to iterate easily over s 
        s = "@" + s + "#"
    
        for j in range(2): 
            rp = 0    # length of 'palindrome radius' 
            R[j][0] = 0
            i = 1
            while i <= n: 
                # Attempt to expand palindrome centered at i 
                while s[i - rp - 1] == s[i + j + rp]: 
                    rp += 1 # Incrementing the length of palindromic 
                            # radius as and when we find valid palindrome 
                # Assigning the found palindromic length to odd/even 
                # length array 
                R[j][i] = rp 
                k = 1
                while (R[j][i - k] != rp - k) and (k < rp): 
                    R[j][i+k] = min(R[j][i-k], rp - k) 
                    k += 1
                rp = max(rp - k, 0) 
                i += k 
    
        # remove guards 
        s = s[1:len(s)-1] 
    
        # Put all obtained palindromes in a hash map to 
        # find only distinct palindrome 
        m[s[0]] = 1
        for i in range(1,n): 
            for j in range(2): 
                for rp in range(R[j][i],0,-1): 
                    m[s[i - rp - 1 : i - rp - 1 + 2 * rp + j]] = 1
            m[s[i]] = 1
        # filter result with palindrome substrings
        count = 0
        strings = []
        for i in m: 
            if len(i) > 1:
                count += 1
                strings.append(i)
        return strings
        
        # printing all distinct palindromes from hash map 
        print(str(count) + " palindrome sub-strings")
    @staticmethod
    def get_json_create_delivery():
        return {
                "shipping_order": {
                    "n_packages": "1",
                    "content_description": "ORDEN 255826267",
                    "imported_id": "255826267",
                    "order_price": "24509.0",
                    "weight": "0.98",
                    "volume": "1.0",
                    "type": "delivery"
                },
                "shipping_origin": { "warehouse_code": "401" },
                "shipping_destination": {
                    "customer": {
                    "name": "Bernardita Tapia Riquelme",
                    "email": "b.tapia@outlook.com",
                    "phone": "977623070"
                    },
                    "delivery_address": {
                        "home_address": {
                            "place": "Puente Alto",
                            "full_address": "SAN HUGO 01324, Puente Alto, Puente Alto"
                        }
                    }
                },
                "carrier": { 
                    "carrier_code": "blx",
                    "tracking_number": ""
                }
            }
    
    @staticmethod
    def fibonacciDelivery(km):
        arrayFib = [0,1]
        days_delivery = 0
        print("N 0 rango : 0 - 100 dias 0")
        if km < 100:
            return 0
        if km < 200 and km >= 100:
            return 1
        print("N 1 rango : 100 - 200 dias 1")
        n = 2
        while True:
            days_delivery = arrayFib[n-1] + arrayFib[n-2]
            arrayFib.append(days_delivery)
            max_range = (n + 1) * 100
            min_range = ((n + 1) * 100) - 100
            print("N "+str(n) + " rango :" +str(min_range)+" - "+str(max_range)+" dias "+str(days_delivery))
            if km >= min_range and km < max_range:
                break
            n+=1
        print(arrayFib)
        return days_delivery
    
    @staticmethod
    def fibonacciDivisors(limit_divisors):
        arrayFib = [0,1]
        n = 2
        while True:
            fibonacci = arrayFib[n-1] + arrayFib[n-2]
            arrayFib.append(fibonacci)
            divisors = Utilities.divisors(fibonacci)
            if len(divisors) > limit_divisors:
                break
            n+=1
        return fibonacci
    
    ##############################################################
    ### cartesian product of lists ##################################
    ##############################################################
    @staticmethod
    def appendEs2Sequences(sequences,es):
        result=[]
        if not sequences:
            for e in es:
                result.append([e])
        else:
            for e in es:
                result+=[seq+[e] for seq in sequences]
        return result

    @staticmethod
    def cartesianproduct(lists):
        return reduce(Utilities.appendEs2Sequences,lists,[])

    ##############################################################
    ### prime factors of a natural ##################################
    ##############################################################
    @staticmethod
    def primefactors(n):
        i = 2
        while i<=sqrt(n):
            if n%i==0:
                l = Utilities.primefactors(n/i)
                l.append(i)
                return l
            i+=1
        return [n]


    ##############################################################
    ### factorization of a natural ##################################
    ##############################################################
    @staticmethod
    def factorGenerator(n):
        p = Utilities.primefactors(n)
        factors={}
        for p1 in p:
            try:
                factors[p1]+=1
            except KeyError:
                factors[p1]=1
        return factors
    
    @staticmethod
    def divisors(n):
        factors = Utilities.factorGenerator(n)
        divisors=[]
        listexponents=[map(lambda x:k**x,range(0,factors[k]+1)) for k in factors.keys()]
        listfactors=Utilities.cartesianproduct(listexponents)
        for f in listfactors:
            divisors.append(reduce(lambda x, y: x*y, f, 1))
        divisors.sort()
        return divisors
    
    @staticmethod
    def isTokenIntegration(token):
        exists_token = False
        for key in app_config[enviroment].TOKENS:
            if app_config[enviroment].TOKENS[key] == token:
                exists_token = True
                break
        return exists_token
