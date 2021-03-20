from linker import app


def start_app_debug():
    """Start the application in debug mode."""

    app.run(debug=True)


def start_app_prod():
    """Start the application in production mode."""

    return app


def db_sync():
    """Run DB sync to create the database."""

    from linker import db
    db.init_db()
