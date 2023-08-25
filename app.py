from flask import Flask
from core import config
from flask_cors import CORS
from models import db
from os import system
from models.register_tables import register_tables
from sys import platform, version, argv
from click import command, option

from flask import Flask
from flask.cli import with_appcontext

from models.register_tables import (register_tables)

from blueprints.users import users_bp


def create_app():
    """
    Create application factory,
    as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.APP_SETTING)
    app.logger.setLevel(config.APP_SETTING.LOG_LEVEL)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    
    return app

def create_worker_app():
    """create worker app without blueprint"""
    app = Flask(__name__)
    app.config.from_object(config.APP_SETTING)
    app.logger.setLevel(config.APP_SETTING.LOG_LEVEL)
    register_extensions(app)
    register_shellcontext(app)
    return app

def register_extensions(app):
    """Register Flask extensions."""
    db.db.init_app(app)
    db.migrate.init_app(app, db.db)
    db.marsh.init_app(app)

    return None

def register_shellcontext(app):
    """Register shell context objects."""
    shell_context = {
        'db': db.db
    }
    shell_context.update(register_tables)

    app.shell_context_processor(lambda: shell_context)

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(users_bp)
    return None

def shells_imported_class():

    # activate color print
    system('color')

    CYAN = '\033[96m'
    GREEN = '\033[92m'
    GREY = '\33[90m'
    ENDC = '\033[0m'
    result = []
    if len(argv) > 1 and argv[1] == "shell_plus":
        for orm_class in register_tables.values():
            result.append(
                f"{GREEN}from{ENDC} {CYAN}"
                f"{orm_class.__module__}{ENDC} "
                f"{GREEN}import{ENDC} {orm_class.__name__}"
            )
        result.append(f"\n{GREY}>>>> shell_plus pre import classes{ENDC}")
        result.append("\n")

    return "\n".join(result) 
    
@command("shell_plus", short_help="Run a shell plus in the app context.")
@option('--print-sql/--no-print-sql', default=False)
@option('--test/--no-test', default=False)
@with_appcontext
def shell_plus_command(print_sql, test):
    """
    shell_plus like django-extensions
    """
    from flask.globals import _app_ctx_stack
    from IPython import InteractiveShell, start_ipython

    app = _app_ctx_stack.top.app
    banner = "Python %s on %s\nApp: %s [%s]\nInstance: %s\n%s" % (
        version,
        platform,
        app.import_name,
        app.env,
        app.instance_path,
        shells_imported_class()
    )
    ctx = {}

    if print_sql:
        app.config.update({
            'SQLALCHEMY_ECHO': True
        })
    if test:
        app.config.update({
            'TESTING': True
        })

    ctx.update(app.make_shell_context())

    InteractiveShell.banner1 = banner
    start_ipython(argv=[], user_ns=ctx)