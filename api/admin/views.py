from flask_restx import Resource, Namespace, fields
from flask import request
from ..models.admin import Admin
from http import HTTPStatus
from werkzeug.security import generate_password_hash



admin_namespace = Namespace('admin', description='Namespace for Admin')

admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'first_name': fields.String(required=True, description="Admin First Name"),
        'last_name': fields.String(required=True, description="Admin Last Name"),
        'email': fields.String(required=True, description="Admin Email"),
        'password': fields.String(required=True, description="Admin Password")

    }
)

@admin_namespace.route('/create_admin')
class CreateAdmin(Resource):
    @admin_namespace.expect(admin_signup_model)
    # Uncomment the @admin_required decorator below after registering the first admin
    # This ensures that only an existing admin can register a new admin account on the app
    # @admin_required
    @admin_namespace.doc(
        description = "Register an Admin"
    )
    def post(self):
        """
            Register an Admin - Admins Only
        """      
        data = request.get_json()
        
        # Create the admin user
        admin_user = Admin(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            is_admin=True
        )

        admin_user.save()


        response = {
                'first_name': admin_user.first_name,
                'last_name': admin_user.last_name,
                'email': admin_user.email
        }

        return response, HTTPStatus.CREATED




