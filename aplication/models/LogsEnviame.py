# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

from aplication.db import db
from aplication.helpers.Utilities import Utilities


class LogsEnviame(db.Model):
    __tablename__ = 'log_enviame'
    __table_args__ = {'schema': 'db'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=True)
    payload = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    #CRUD

    @classmethod
    def get_data(cls, _id):
        query =  cls.query.filter_by(id=_id).first()
        return  Utilities.get_structure(query) if query is not None else None
    
    @classmethod
    def get_all(cls):
        query =  cls.query.all()
        return  Utilities.get_structure(query) if query is not None else None

    @classmethod
    def insert_data(cls, dataJson):
        query = LogsEnviame( 
            name = dataJson['name'],
            status = dataJson['status'] if "status" in dataJson else 0,
            payload = dataJson['payload'],
            response = dataJson['response'] if "response" in dataJson else None
            )
        LogsEnviame.save(query)
        if query.id:                            
            return  Utilities.get_structure(query)
        return  None

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'name' in dataJson:
                query.name = dataJson['name']
            if 'status' in dataJson:
                query.status = dataJson['status']
            if 'payload' in dataJson:
                query.payload = dataJson['payload']
            if 'response' in dataJson:
                query.response = dataJson['response']
            db.session.commit()
            if query.id:                            
                return Utilities.get_structure(query)
        return  None

    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            LogsEnviame.delete(query)
            if query.id:                            
                return query.id
        return  None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

