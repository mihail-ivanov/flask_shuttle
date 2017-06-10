from setuptools import setup, find_packages
import flask_shuttle


entry_points = {
    'console_scripts': [
        "fshuttle = flask_shuttle.cli:main",
    ]
}


with open('requirements.txt') as f:
    requires = [l for l in f.read().splitlines() if l]


setup(
    name='Flask-Shuttle',
    version=flask_shuttle.__version__,
    packages=['flask_shuttle'],
    include_package_data=True,
    description='Flask application generator.',
    url='https://github.com/mihail-ivanov/flask_shuttle',
    author='Mihail Ivanov',
    author_email='mihail@muplextech.com',
    license='MIT',
    keywords='flask app generator',
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
