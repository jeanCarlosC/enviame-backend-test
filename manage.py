#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from app.app import app,db

manager = Manager(app)
app.config['DEBUG'] = True # Ensure debugger will load.

@manager.command
def create_tables():
    "Crear tablas en la base de datos."
    db.create_all()
    db.session.commit()

@manager.command
def drop_tables():
    "Eliminar todas las tablas relacionadas de la base de datos."
    db.drop_all()


if __name__ == '__main__':
    manager.run()
