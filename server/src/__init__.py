#import flask
from flask import Flask
from flask_cors import CORS

import uuid

# Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.

# from .config import config
# CHECK https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/
# using the current set-up

# def create_app(config_mode):
# Error: Detected factory 'create_app' in module 'src', but could not call it without arguments. Use 'src:create_app(args)' to specify arguments.


#from collections import OrderedDict
#import json

#class JSONEncoder(json.JSONEncoder):

    #def default(self, o):
        #def recursive(p):
            #result = OrderedDict()
            #for k in p.keys():
                #result[k] = getattr(o, k)
                #if isinstance(result[k], dict):
                    #result[k] = recursive(result[k])
                #if isinstance(result[k], datetime):
                    #result[k] = result[k].timestamp()
            #return result

        #if isinstance(o, Model):
            #return dict(recursive(o.__mapper__.c))
        #return flask.json.JSONEncoder.default(self, o)



def create_app():
    
    app = Flask(__name__)
    
    #app.secret_key = str(uuid.uuid4())
    app.config['SECRET_KEY'] = str(uuid.uuid4())
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    
    CORS(app)
    
    #app.json_encoder = JSONEncoder
        
    # config_mode unused now
    # app.config.from_object(config[config_mode])
    
    from .db import Session, init
    # how do we access models?
    init()
    
    # does this goes here?
    @app.teardown_appcontext
    def cleanup(exception=None):
        Session.remove()
    
    return app
