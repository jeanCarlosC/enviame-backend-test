class Config(object):
    SECRET_KEY = 'f0faa2bed03b28e48544762d760aa169'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    PATH_STORAGE = "/app/upload"
    ROOT_PATH = "/app"
    TIME_SESSION = 60000

class DevelopmentConfig(Config):
    """
    Development configurations 
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root12345@dbmysql:3306/db"
    URLS_ENVIAME = {
        'create_delivery': 'https://stage.api.enviame.io/api/s2/v2/companies/401/deliveries'
    }
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE = 160

class TestingConfig(Config):
    """
    Testing configurations 
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://enviame:enviame12345@dbmysql:3306/db"
    URLS_ENVIAME = {
        'create_delivery': 'https://stage.api.enviame.io/api/s2/v2/companies/401/deliveries'
    }
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE=160
    



class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = ""
    JSON_AS_ASCII = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE=160
    


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
