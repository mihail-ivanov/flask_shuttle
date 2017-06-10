
from .development import DevelopmentConfig
from .testing import TestingConfig
from .production import ProductionConfig


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
