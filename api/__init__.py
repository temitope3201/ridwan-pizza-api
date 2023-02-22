from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed, Forbidden



def create_app(config = config_dict['dev']):
    app = Flask(__name__)
    authorizations ={
        "Bearer Auth":{
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description":"Add a JWT token to the Header with **Bearer&lt;JWT&gt token to authorize"
        }
    }
    api = Api(app, 
        title="Pizza Delivery API", 
        description="A simple Pizza delivery REST API service",
        version=1.0,
        authorizations= authorizations,
        security="Bearer Auth"
        )

    app.config.from_object(config)
    db.init_app(app)

    jwt = JWTManager(app)
    migrate = Migrate(app,db)


    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):

        return {"error": "Not Found"}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):

        return {"error": "Method Not Allowed"}, 405

    @api.errorhandler(Forbidden)
    def forbidden(error):

        return {"error": "Forbidden"}, 403

    @app.shell_context_processor
    def make_shell_context():

        return{
            'db': db,
            'user': User,
            'order': Order
        }

    return app