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
    def getPalindromes(s):
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
    
        count = 0
        strings = []
        return m
        for i in m: 
            if len(i) > 1:
                count += 1
                print(i) 
        
        # printing all distinct palindromes from hash map 
        print("Below are " + str(count) + " pali sub-strings")

    
    @staticmethod
    def fibonacci(limit):
        arrayFib = [0,1]
        while len(arrayFib) <= limit:
            n = len(arrayFib)
            number_fibonacci = arrayFib[n-1] + arrayFib[n-2]
            arrayFib.append(number_fibonacci)

            print("Fibonacci "+str(number_fibonacci))
        return arrayFib
    @staticmethod
    def dividers(number):
        dividers = []
        for i in range(1, number+1):
            if number % i == 0:
                dividers.append(i)
        return dividers

    @staticmethod
    def getFibonacciNumber():
        number = 1;
        i = 2;
        cnt = 0;
        Dn1 = 2;
        Dn = 2;
        fibList = Utilities.fibonacci(100)
        
        while cnt < 11 :
            if i % 2 == 0:
                Dn = Utilities.PrimeFactorisationNoD(i + 1, fibList)
                cnt = Dn * Dn1
            else:
                Dn1 = Utilities.PrimeFactorisationNoD((i + 1) / 2, fibList)
                cnt = Dn*Dn1
            i+=1
        return i * (i - 1) / 2

    @staticmethod
    def PrimeFactorisationNoD(number, fibList):
        nod = 1
        remain = number
    
        for item_fibList in fibList: 
            if item_fibList > 1:
                if (item_fibList * item_fibList > number):
                    return nod * 2
                exponent = 1
                while (remain % item_fibList == 0):
                    exponent+=1
                    remain = remain / item_fibList

                nod *= exponent
        
                if remain == 1 :
                    return nod
            return nod

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