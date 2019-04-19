""" Module for seed cli subgroup

$ FLASK_APP=app flask seed <command>
"""

import os
import re
import importlib
import inspect
import click
from flask.cli import with_appcontext
from flask import current_app as app

from flask_seeder import Seeder

def get_seed_scripts(root="seeds"):
    """ Get seed scripts

    Recursively walk a directory structure and find all python scripts.

    Arguments:
        root: Optional root directory to start walking (Default: "seeds")

    Returns:
        Returns a list with python module paths in the format "package.module".
        If no files are found, and empty list is returned.

    """
    extension = "py"
    result = []
    for path, _, files in os.walk(root):
        for filename in files:
            if not re.search(r"\."+extension+"$", filename):
                continue

            # Strip file extension
            filename = re.sub(r"\."+extension+"$", "", filename)

            # Concat the full file path
            file_path = os.path.join(path, filename)

            # Replace filesystem separator with python module separator
            if os.path.sep == "\\":
                mod_path = re.sub(r"\\", ".", file_path)
            else:
                mod_path = re.sub(os.path.sep, ".", file_path)

            result.append(mod_path)
    return result

def inheritsfrom(child, parent):
    """ Verify inheritance

    Check if child inherits from parent. Does the same thing as built-in
    issubclass() except child and parent can't be the same class.

    Arguments:
        child: Child class
        parent: Parent class

    Returns:
        Returns True if Child inherits from Parent.
        Returns False if Child does not inherit from Parent or if Child and Parent
        is the same class.
    """
    return issubclass(child, parent) and child != parent

def load_seeder(cls, name, mod_path, file_path):
    """ Load seeder instance

    Instantiate a seeder using common base settings.

    Arguments:
        cls: Seeder class
        name: String name representation of the seeder
        mod_path: Python module path (package.module)
        file_path: Path to the python file in the file system

    Returns:
        Returns an instance of `cls`.
    """
    seeder = cls()
    seeder.name = name
    seeder.mod_path = mod_path
    seeder.file_path = file_path

    return seeder

def get_seeders_in_script(script):
    """ Get all seeders in a script file

    Reads a python script and detecs all classes within that inherits from the base Seeder class.

    Arguments:
        script: Filesystem path to the script

    Returns:
        Returns a list of loaded seeder objects from the script
    """
    seeders = []
    module = importlib.import_module(script)
    members = inspect.getmembers(module, inspect.isclass)
    for member in members:
        if inheritsfrom(member[1], Seeder):
            seeder = load_seeder(member[1], member[0], script, "")
            seeders.append(seeder)

    return seeders

def get_seeders(root=None):
    """ Get all seeders from all scripts

    Finds all python scripts with seeders, loads them and return them.

    Returns:
        List of loaded seeder objects
    """
    seeders = []
    if root is not None:
        scripts = get_seed_scripts(root=root)
    else:
        scripts = get_seed_scripts()

    for script in scripts:
        seeders.extend(get_seeders_in_script(script))

    return seeders


@click.group()
def seed():
    """ Database seed commands """

@seed.command("run")
@click.option("--root", default="seeds", type=click.Path(), help="Root directory for seed scripts")
@with_appcontext
def seed_run(root):
    """ Run database seeders """
    click.echo("Running database seeders")
    db = None
    try:
        db = app.extensions["flask_seeder"].db
    except KeyError:
        raise RuntimeError("Flask-Seeder not initialized!")

    for seeder in get_seeders(root=root):
        seeder.db = db
        try:
            seeder.run()
        # pylint: disable=bare-except
        except:
            click.echo("%s...\t[ERROR]" % seeder.name)
            continue

        click.echo("%s...\t[OK]" % seeder.name)


@seed.command("list")
@click.option("--root", default="seeds", type=click.Path(), help="Root directory for seed scripts")
def seed_list(root):
    """ List all discoverable seeders """
    for seeder in get_seeders(root=root):
        click.echo("* %s" % seeder.name)
