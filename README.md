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

When all seeders have completed (successfully or not), Flask-Seeder will by default commit all changes to the database. This behaviour can be overridden with `--no-commit` or setting environment variable `FLASK_SEEDER_AUTOCOMMIT=0`.

## Run Order

When splitting seeders across multiple classes and files, order of operations is determined by two factors.
First the seeders are grouped by `priority` (lower priority will be run first), all seeders with the same priority
are then ordered by class name.

See example below for setting priority on a seeder.

```python
from flask_seeder import Seeder

class DemoSeeder(Seeder):
  def __init__(self, db=None):
    super().__init__(db=db)
    self.priority = 10

  def run(self):
    ...
```

# Faker and Generators
Flask-Seeder provides a `Faker` class that controls the creation of fake objects, based on real models. By telling `Faker` how to create the objects, you can easily create many different unique objects to help when seeding the database.

There are different generators that help generate values for the fake objects.
Currently supported generators are:

* Integer: Create a random integer between two values
* UUID: Create a random UUID
* Sequence: Create integers in sequence if called multiple times
* Name: Create a random name from a list `data/names/names.txt`
* Email: Create a random email, a combination of the random name generator and a domain from `data/domains/domains.txt`
* String: String generation from a pattern

Feel free to roll your own generator by subclassing `Generator` and implement a `generate()` method that return the generated value.

## String generator pattern
The `String` generator takes a pattern and produces a string that matches the pattern.
Currently the generator pattern is very simple and supports only a handful of operations.

| Pattern | Produces | Description | Example |
| --| -- | -- | -- |
| [abc] | String character | Randomly select one of the provided characters | `b` |
| [a-k] | String character | Randomly select one character from a range | `i` |
| \c | String character | Randomly select any alpha character (a-z, A-Z) | `B` |
| (one\|two) | String group | Like `[abc]` but works for strings, not just single characters | `one` |
| \d | Digit | Randomly select a single digit (0-9) | `8` |
| {x} | Repeater | Repeat the previous pattern `x` times | `\d{5}` |
| {m,n} | Repeater | Repeat the previous pattern `x` times where `x` is anywhere between `m` and `n` | `[0-9]{2,8}` |
| abc | String literal | No processing, returned as is | `abc` |

Patterns can also be combined to produce more complex strings.
```
# Produces something like: abc5586oz
abc[5-9]{4}\c[xyz]
```

# Example usage
Examples show only relevant snippets of code

**app.py:**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder

def create_app():
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
  def __init__(self, id_num=None, name=None, age=None):
    self.id_num = id_num
    self.name = name
    self.age = age

  def __str__(self):
    return "ID=%d, Name=%s, Age=%d" % (self.id_num, self.name, self.age)

# All seeders inherit from Seeder
class DemoSeeder(Seeder):

  # run() will be called by Flask-Seeder
  def run(self):
    # Create a new Faker and tell it how to create User objects
    faker = Faker(
      cls=User,
      init={
        "id_num": generator.Sequence(),
        "name": generator.Name(),
        "age": generator.Integer(start=20, end=100)
      }
    )

    # Create 5 users
    for user in faker.create(5):
      print("Adding user: %s" % user)
      self.db.session.add(user)
```

***Shell***
```bash
$ flask seed run
Running database seeders
Adding user: ID=1, Name=Fancie, Age=76
Adding user: ID=2, Name=Shela, Age=22
Adding user: ID=3, Name=Jo, Age=33
Adding user: ID=4, Name=Laureen, Age=54
Adding user: ID=5, Name=Tandy, Age=66
DemoSeeder... [OK]
Committing to database!
```
