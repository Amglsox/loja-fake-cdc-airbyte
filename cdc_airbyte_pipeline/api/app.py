import logging

from flask import Flask
from routes.resources import routes


logger = logging.getLogger()
logger.level = logging.DEBUG


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config["DEBUG"] = True
    app.config.from_object("conf.Config")
    with app.app_context():
        app.register_blueprint(routes)
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="7990")
