from flask import Flask
from flask_sitemapper import Sitemapper

app = Flask(__name__)
sitemapper = Sitemapper()
sitemapper.init_app(app)
# app.config['SERVER_NAME'] = 'bolognamagica.com'

from webapp import routes

