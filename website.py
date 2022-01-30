#!/usr/bin/python
#-*- encoding:utf-8 -*-

import threading
from flask import Flask
from spaghetti_code import Spaghetti_Monster

app  = Flask(__name__)
threading.Thread(target=Spaghetti_Monster, daemon=True).start()

# PAGES
@app.route("/")
def index():
    return {"status":"running."}

@app.errorhandler(404)
def not_found(error):
    return {"error":"Page not found."}, 404