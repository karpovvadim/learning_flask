import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application
    (Создайте и настройте экземпляр приложения Flask)."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        # (секрет по умолчанию, который должен быть переопределен конфигурацией экземпляра)
        SECRET_KEY="dev",
        # store the database in the instance folder (сохранить базу данных в папке экземпляра)
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # (загрузить конфигурацию экземпляра, если она существует, когда не тестируется)
        app.config.from_pyfile("config.py", silent=True)
    else:
# load the test config if passed in (загрузить тестовую конфигурацию, если она была передана)
        app.config.update(test_config)

    # ensure the instance folder exists (убедитесь, что папка экземпляра существует)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands (зарегистрировать команды базы данных)
    from flaskr import db
    db.init_app(app)

    # apply the blueprints to the app (применить чертежи к приложению)
    from flaskr import auth, blog

    app.register_blueprint(auth.bp)

    return app
