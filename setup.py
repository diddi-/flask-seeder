"""
Flask-Script-Seed
-------------

"""
from setuptools import setup

setup(
    name="Flask-Script-Seed",
    version="0.0.1",
    url="",
    author="Diddi Oscarsson",
    author_email="diddi.oscarsson@telenor.se",
    description="Flask extension to seed database through scripts",
    long_description=__doc__,
    packages=['flask_seeder'],
    include_package_data=True,
    install_requires=[
        "Flask",
        "Flask-SQLAlchemy"
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
