from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

blacklist = set()

auth_namespace = Namespace('auth', description='Namespace for authentication') 


login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password")
    }
)


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT Token/Login
         """
        data = request.get_json()

        email = data['email']
        password = data['password']
        
        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        pass


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Generate an Access Token
        """
        user = get_jwt_identity()

        access_token = create_access_token(identity=user)

        return {'access_token': access_token}, HTTPStatus.OK
    

@auth_namespace.route('/logout')
class LogOut(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        """
            Returns "Access token revoked" or "Refresh token revoked" depending on the token type"
        """
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        blacklist.add(jti)
        return {"message":f"{ttype.capitalize()} token revoked succesfully"}, HTTPStatus.OK




