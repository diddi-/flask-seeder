# Flask-Seeder
[![Build Status](https://travis-ci.org/diddi-/flask-seeder.svg?branch=master)](https://travis-ci.org/diddi-/flask-seeder)

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
from flask_seeder import Seeder

# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder after instantiating the class
  def run(self):
    self.db.session.add(...) # Standard SQLAlchemy add
    self.db.session.commit()
```

***Shell***
```bash
$ flask seed run
Running database seeders
DemoSeeder... [OK]
```
