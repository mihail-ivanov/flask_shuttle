
import random

from flask_script import Command


class SecretKeyCommand(Command):
    """Generates secret key"""

    def run(self):
        """
        Create a random secret key.

        Taken from the Django project.
        """
        random_generator = random.SystemRandom()
        length = 50
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)'
        return ''.join(random_generator.choice(chars) for i in range(length))
