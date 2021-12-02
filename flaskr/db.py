# The application will use sqlite database to store
# users and posts. Python comes with built-in support
# for SQLite in the sqlite3 module.
# SQLite is convenient because it doesn't require setting up a
# seperate database server and is built-in to Python.
# However, if concurrent requests try to write to the database
# at the same time,they will slow down as each write
# happens sequentially.small applications won't notice this.
# Once you become big,you may want to switch to a different database.


# Connect to the Database
import sqlite3

import click
from click.core import Context
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
