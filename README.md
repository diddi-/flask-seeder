# Flask-Seeder
[![Build Status](https://travis-ci.org/diddi-/flask-seeder.svg?branch=master)](https://travis-ci.org/diddi-/flask-seeder)
[![Coverage Status](https://coveralls.io/repos/github/diddi-/flask-seeder/badge.svg?branch=master)](https://coveralls.io/github/diddi-/flask-seeder?branch=master)

Flask-Seeder is a Flask extension to help with seeding database with initial data, for example when deploying an application for the first time.

This extensions primary focus is to help populating data once, for example in a demo application where the database might get wiped over and over but you still want users to have some basic data to play around with.


# Installation

```
pip install Flask-Seeder
```
This will install the Flask-Seeder extension and add a `flask seed` subcommand, check it out to see what arguments are supported!

# Seeders
Flask-Seeder provides a base class `Seeder` that holds a database handle.
By subclassing `Seeder` and implementing a `run()` method you get access to the database handle object and can start seeding the database with data.

All seeders must be somewhere in the `seeds/` directory and inherit from `Seeder` or else they won't be detected.

# Faker and Generators
Flask-Seeder provides a `Faker` class that controls the creation of fake objects, based on real models. By telling `Faker` how to create the objects, you can easily create many different unique objects to help when seeding the database.

There are different generators that help generate values for the fake objects.
Currently supported generators are:
* Integer: Create a random integer between two values
* Name: Create a random name from a list `data/names/names.txt`

Feel free to roll your own generator by subclassing `Generator` and implement a `generate()` method that return the generated value.

# Example usage
Examples show only relevant snippets of code

**app.py:**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder

create_app():
  app = Flask(__name__)

  db = SQLAlchemy()
  db.init_app(app)

  seeder = FlaskSeeder()
  seeder.init_app(app, db)

  return app
```

**seeds/demo.py:**
```python
from flask_seeder import Seeder, Faker, generator

# SQLAlchemy database model
class User(Base):
  def __init__(self, name=None, age=None):
    self.name = name
    self.age = age


# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=User,
      init={
        "name": generator.Name(),
        "age": generator.Integer(start=20, end=100)
      }
    )

    # Create 5 users
    for user in faker.create(5):
      self.db.session.add(user)
    self.db.session.commit()
```

***Shell***
```bash
$ flask seed run
Running database seeders
DemoSeeder... [OK]
```
