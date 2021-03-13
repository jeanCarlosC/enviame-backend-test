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
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://enviame:enviame12345@dbmysql:3306/db"
    SQLALCHEMY_POOL_RECYCLE = 200
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATH_STORAGE = "/app/upload"
    ROOT_PATH = "/app"
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE=160

class TestingConfig(Config):
    """
    Testing configurations 
    """
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://jean:12345@dbmysql:3306/db"
    SQLALCHEMY_POOL_RECYCLE = 200
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATH_STORAGE = "/app/upload"
    ROOT_PATH = "/app"
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE=160
    



class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = ""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATH_STORAGE = "/app/upload"
    ROOT_PATH = "/app"
    TIME_SESSION = 60000
    SQLALCHEMY_POOL_RECYCLE=160
    


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
