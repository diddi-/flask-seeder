"""
Flask-Seeder
-------------

"""
from setuptools import setup

setup(
    name="Flask-Seeder",
    version="0.0.1",
    url="https://github.com/diddi-/flask-seeder",
    author="Diddi Oscarsson",
    author_email="diddi@diddi.se",
    description="Flask extension to seed database through scripts",
    long_description=__doc__,
    packages=['flask_seeder'],
    include_package_data=True,
    license = "MIT",
    install_requires=[
        "Flask",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "flask.commands": [
            "seed=flask_seeder.cli:seed",
        ]
    }
)
