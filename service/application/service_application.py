from flask import Flask
import os

service_application = Flask("application")

service_application.config.from_object('settings.default_settings')
if os.environ.get('SPORTKY_SERVICE_SETTINGS', None) != None:
    service_application.config.from_envvar('SPORTKY_SERVICE_SETTINGS')
