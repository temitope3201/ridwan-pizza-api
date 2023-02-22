from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth', description='namespace for authentication')

signup_model = auth_namespace.model(
    'SignUp',{
        'id': fields.Integer(),
        'username': fields.String(required = True, description = 'A Username'),
        'email': fields.String(required = True, description = 'User Email'),
        'password': fields.String(required = True, description = 'Password Input')
    }
)


user_model = auth_namespace.model(
    'User',{
        'id': fields.Integer(),
        'username': fields.String(required = True, description = 'A Username'),
        'email': fields.String(required = True, description = 'User Email'),
        'password_hash': fields.String(required = True, description = 'Password Input'),
        'is_active': fields.Boolean(description = 'Is A user active'),
        'is_staff': fields.Boolean(description = 'Is A user a staff')

    }
)

login_model = auth_namespace.model(
    'Login',{
        'email': fields.String(required = True, description = 'User Email'),
        'password': fields.String(required = True, description = 'User Password')
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description = "Sign up a User")
    def post(self):
        """
            Sign up a User
        """
        data = request.get_json()

        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    @auth_namespace.doc(description = "generate User token")
    def post(self):
        """
            generate User token

        """
        
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        

        user = User.query.filter_by(email = email).first()

        if user is not None and check_password_hash(user.password_hash, password):

            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)

            

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.CREATED

@auth_namespace.route('/refresh')
class Refresh(Resource):

    @jwt_required(refresh = True)
    @auth_namespace.doc(description = "Refresh User token")
    def post(self):

        username = get_jwt_identity()

        access_token = create_access_token(identity = username)

        return {'username': username,
                'access_token': access_token
        }




