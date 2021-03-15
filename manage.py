#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_script import Manager
from aplication.app import app,db

manager = Manager(app)
aplication.config['DEBUG'] = True # Ensure debugger will load.


if __name__ == '__main__':
    manager.run()
