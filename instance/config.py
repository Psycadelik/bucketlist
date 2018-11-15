# /instance/config.py
import os

class Config(object):
	""" Parent Configuration Class ."""
	DEBUG = False
	CSRF_ENABLED = True
	SECRET = os.getenv('SECRET')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bucketlist.db')

class DevelopmentConfig(Config):
	""" Configuration for Development """
	DEBUG = True 
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/test_db'

class TestingConfig(Config):
	"""Configurations for testing, with a separate test database. """

	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/test_db'
	DEBUG = True

class StagingConfig():
	""" Configurations for staging."""
	DEBUG = True

class ProductionConfig(Config):
	""" configurations for Production """
	DEBUG = False
	TESTING = False

app_config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,
	'default':ProductionConfig
}