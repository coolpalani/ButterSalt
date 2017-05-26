import logging
from logging import FileHandler
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from ButterSalt.saltapi import SaltApi

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)
moment = Moment(app)
CSRFProtect(app)
db = SQLAlchemy(app)
mail = Mail(app)


salt = SaltApi(
    app.config.get('SALT_API'),
    app.config.get('USERNAME'),
    app.config.get('PASSWORD')
)


file_handler = FileHandler('ButterSalt.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

from ButterSalt.views.cmdb import cmdb
from ButterSalt.views.saltstack import saltstack
from ButterSalt.views.user import user
from ButterSalt.views.home import home
app.register_blueprint(cmdb)
app.register_blueprint(saltstack)
app.register_blueprint(user)
app.register_blueprint(home)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
