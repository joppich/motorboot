import os
import yaml

"""
Settings for motorboot app
===========================================
"""

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_MODE = os.environ.get('FLASK_APP_MODE',
                              'default')
    SECRET_KEY= os.environ.get('FLASK_APP_KEY',
                               'default')
    LOGPATH = os.environ.get('FLASK_APP_LOGDIR',
                             'default')
    if LOGPATH == 'default':
        LOGPATH = os.path.join(basedir,'logs')
    else:
        LOGPATH = os.path.abspath(LOGPATH)
    if not os.path.exists(LOGPATH):
        os.mkdir(LOGPATH)
    LOGFILE = os.path.join(LOGPATH,
                           'motorboot_{}.log'.format(APP_MODE)
                          )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SECRETSFILE = os.path.abspath(os.environ.get('APPSECRETS','.secrets'))
    if os.path.isfile(SECRETSFILE):
        with open(SECRETSFILE) as _f:
            TOKEN = yaml.safe_load(_f)
    else:
        TOKEN = {'testtoken':'testuser'}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_dev.sqlite'))


class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_prod.sqlite'))

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ \
            os.path.join(basedir,'{}'.format('mb_test.sqlite'))
    DEBUG=True
    TESTING=True
    SERVER_NAME='motorboot_test'
    FLASK_COVERAGE = 1


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,

        'default': DevelopmentConfig
        }
