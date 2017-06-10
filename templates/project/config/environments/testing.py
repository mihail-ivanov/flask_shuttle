
import os

from .default import DefaultConfig


class TestingConfig(DefaultConfig):
    """
    Testing configuration
    """

    DEBUG = False
    TESTING = True

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DefaultConfig.BASE_DIR, 'instance', 'testing.db')
    DATABASE_CONNECT_OPTIONS = {}
    SQLALCHEMY_ECHO = False
