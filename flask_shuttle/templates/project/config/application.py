
import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .evironments import app_config


class Application(object):
    def __init__(self):
        self.app = self._create_app()
        self.db = self._create_db(self.app)
        self.migrate = self._create_migrations(self.app, self.db)

        self._configure_error_handlers(self.app)

    #
    # Create Flask application
    #
    def _create_app(self):
        app = Flask(
            __name__,
            instance_relative_config=True,
            static_url_path='/static',
            static_folder='../static'
        )

        app.config.from_object(app_config[self._config_name()])
        app.config.from_pyfile('config.py')

        return app

    def _create_db(self, app):
        return SQLAlchemy(app)

    def _create_migrations(self, app, db):
        return Migrate(app, db)

    def _config_name(self):
        return os.getenv('FLASK_CONFIG') or 'development'

    def _configure_error_handlers(self, app):
        @app.errorhandler(404)
        def not_found(error):
            return (render_template('404.html'), 404)

        @app.route('/favicon.ico')
        def favicon():
            return ''






# from flask_assets import Environment






# def create_app(config_name=None):

#     assets = configure_assets(app)

#     configure_error_handlers(app)
#     configure_blueprints(app)

#     # Migrations
#
#     from app import models

#     return app


# def configure_assets(app):
#     from .assets import ASSET_DIRS
#     from .assets import ASSETS

#     # Configure flask assets
#     assets = Environment(app)

#     app_dir = app.config['BASE_DIR']
#     current_dir = os.path.dirname(os.path.realpath(__file__))

#     assets.set_directory(os.path.join(app_dir, 'static'))

#     for asset_dir in ASSET_DIRS:
#         assets.append_path(os.path.join(current_dir, asset_dir))

#     for asset_name, asset in ASSETS.items():
#         assets.register(asset_name, asset)

#     return assets


# def configure_blueprints(app):
#     from .views import register_views
#     register_views(app)
