import os

class DevEnv(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URI = os.getenv("DEVELOPMENT_DB_URL")
class TestEnv(Config):
    TESTING = True
    DATABASE_URI = os.getenv("TEST_DB_URL")
class ProductionEnv(Config):
    DEBUG = False
    DATABASE_URI = os.getenv("PRODUCTION_DB_URL")
config = {
    "development": DevEnv,
    "testing": TestEnv,
    "production": ProductionEnv
}
