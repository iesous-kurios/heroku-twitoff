"""Flask app configurations for local development and production."""
import os
from decouple import config


class Config:
    """Base config common for all environments."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI')

class DevelopmentConfig(Config):
    """Config for local usage with SQLite."""
    DEBUG = True

class ProductionConfig(Config):
    """Config for deploying to Heroku."""
    pass

class TestingConfig(Config):
    """Config for running any tests."""
    TESTING = True
