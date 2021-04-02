# import click
# from flask.cli import with_appcontext
from app import db
# from flask_migrate import Migrate
# migrate = Migrate(app, db)
#
#
# @click.command(name='init_db')
# create all db tables
# @app.before_first_request
# @with_appcontext
# def init_db():
db.create_all()
