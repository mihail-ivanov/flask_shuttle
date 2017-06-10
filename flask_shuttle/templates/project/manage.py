
# Ensure external libs path is added
import sys
sys.path.append('libs')


from config.application import Application
from flask_shuttle.commands import command_manager


if __name__ == "__main__":
    application = Application()
    command_manager.app = application.app
    command_manager.run()
