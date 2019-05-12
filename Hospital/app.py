"""
This script runs the application using a development server.
"""
import bottle
import os
import sys

# routes contains the HTTP handlers for our server and must be imported.
import routes
import dataaccess

from bottle import response
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="HOST for start")
parser.add_argument("--port", help="PORT for start")
parser.add_argument("--dbhost", help="HOST database")
parser.add_argument("--dbport", help="PORT database")
parser.add_argument("--dbuser", help="USER database")
parser.add_argument("--dbpass", help="PASSWORD for USER database")
parser.add_argument("--dbname", help="NAME of database")
args = parser.parse_args()



class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers 
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Accept-Language, auth_token'
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)
            else:
                return None

        return _enable_cors

app = bottle.app()
app.install(EnableCors())
if __name__ == '__main__':
    HOST="localhost"
    PORT=5555
    DB_HOST = "localhost"
    DB_PORT = "3306"
    DB_USER = "root"
    DB_PASS = ""
    DB_NAME = "hospital"
    if(not args.host is None):
        HOST = args.host
    if(not args.port is None):
        PORT = args.port
    
    if(not args.dbhost is None):
        DB_HOST = args.dbhost
    if(not args.dbport is None):
        DB_PORT = args.dbport
    if(not args.dbuser is None):
        DB_USER = args.dbuser
    if(not args.dbpass is None):
        DB_PASS = args.dbpass
    if(not args.dbname is None):
        DB_NAME = args.dbname

    dataaccess.set_settings(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)
    bottle.run(host=HOST, port=PORT)
