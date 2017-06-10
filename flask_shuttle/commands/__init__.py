
from flask_script import Manager


# Import and use this manager
command_manager = Manager()


# If flask assets is installed - load assets command
try:
    from flask_assets import ManageAssets

    command_manager.add_command('assets', ManageAssets())
except ImportError:
    pass


# If flask migrate is installed - load migrate command
try:
    from flask_migrate import MigrateCommand

    command_manager.add_command('db', MigrateCommand)
except ImportError:
    pass


from .routes import RoutesCommand
command_manager.add_command('routes', RoutesCommand())


from .secret_key import SecretKeyCommand
command_manager.add_command('secret_key', SecretKeyCommand())


from .vendor import VendorManager
command_manager.add_command('vendor', VendorManager)
