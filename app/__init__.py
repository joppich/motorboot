import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from logging.handlers import RotatingFileHandler
from settings import config

db = SQLAlchemy()

def create_app(cnf=None):
    '''
        Create skeleton application...
    '''
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if cnf:
        app.config.from_object(config[cnf])
        config[cnf].init_app(app)

    db.init_app(app)

    if not app.debug:
        loghandler = RotatingFileHandler(app.config['LOGPATH'] +\
                                         'motorboot.log',
                                         maxBytes=10000,
                                         backupCount=2
                                        )
        loghandler.setLevel(logging.INFO)
        app.logger.addHandler(loghandler)

    from .bootfiles import bp as bootfiles_blueprint
    app.register_blueprint(bootfiles_blueprint, url_prefix='/api/v1/bootfiles')

    from .bootconf import bp as bootconf_blueprint
    app.register_blueprint(bootconf_blueprint, url_prefix='/api/v1/bootconf')

    return app
