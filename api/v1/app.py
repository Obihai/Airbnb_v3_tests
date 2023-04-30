#!/usr/bin/python3
"""
creating an api
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

db_host = getenv('HBNB_API_HOST')
db_port = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def tear_down(exc):
    """ close a data base session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ method for when page requested is not found"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=db_host if db_host else '0.0.0.0',
            port=db_port if db_port else '5000',
            threaded=True, debug=1)
