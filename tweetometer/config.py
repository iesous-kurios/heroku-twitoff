"""Flask app configurations for local development and production."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base config common for all environments."""
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI')

class DevelopmentConfig(Config):
    """Config for local usage with SQLite."""
    DEBUG = True

class ProductionConfig(Config):
    """Config for deploying to Heroku."""
    pass

class TestingConfig(Config):
    """Config for running any tests."""
    TESTING = True
