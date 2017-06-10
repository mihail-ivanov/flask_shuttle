
import os

from .default import DefaultConfig


class ProductionConfig(DefaultConfig):
    """
    Production configuration
    """

    DEBUG = False

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DefaultConfig.BASE_DIR, 'instance', 'production.db')
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_ECHO = False
