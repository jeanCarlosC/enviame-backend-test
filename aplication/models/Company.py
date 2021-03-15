# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Index, Integer, String, Table, Text, Time
from sqlalchemy.schema import FetchedValue
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.enumerated import ENUM
from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()

from aplication.db import db
from aplication.helpers.Utilities import Utilities


class Company(db.Model):
    __tablename__ = 'company'
    __table_args__ = {'schema': 'db'}

    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    mail = db.Column(db.Integer, nullable=True)
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
    def get_data_by_identification(cls, _identification):
        query =  cls.query.filter_by(identification=_identification).first()
        return  Utilities.get_structure(query) if query is not None else None

    @classmethod
    def insert_data(cls, dataJson):
        query = Company( 
            identification = dataJson['identification'],
            name = dataJson['name'],
            address = dataJson['address'],
            status = dataJson['status'] if "status" in dataJson else 1,
            phone = dataJson['phone'] if "phone" in dataJson else None,
            mail = dataJson['mail'] if "mail" in dataJson else None
            )
        Company.save(query)
        if query.id:                            
            return  Utilities.get_structure(query)
        return  None

    @classmethod
    def update_data(cls, _id, dataJson):
        query = cls.query.filter_by(id=_id).first()
        if query:
            if 'identification' in dataJson:
                query.identification = dataJson['identification']
            if 'name' in dataJson:
                query.name = dataJson['name']
            if 'address' in dataJson:
                query.address = dataJson['address']
            if 'status' in dataJson:
                query.status = dataJson['status']
            if 'phone' in dataJson:
                query.phone = dataJson['phone']
            if 'mail' in dataJson:
                query.mail = dataJson['mail']
            db.session.commit()
            if query.id:                            
                return Utilities.get_structure(query)
        return  None

    @classmethod
    def delete_data(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            Company.delete(query)
            if query.id:                            
                return query.id
        return  None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

