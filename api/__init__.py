from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
from .courses.views import course_namespace
from .auth.views import auth_namespace
from .student.views import student_namespace
from .admin.views import admin_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.users import User
from .models.admin import Admin
from .models.score import Score
from .models.enrollment import Enrollment
from .models.student import Student
from flask_migrate import Migrate 
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    load_dotenv()

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    authorizations = {
       "Bearer Auth": {
           "type": "apiKey",
            "in": "header",
            "name": "Authorization",
           "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    description = (
        'A Student Management REST API service. \n'
        'Repository: https://github.com/Ruona-Ewh/School-Management--API'
    )


    api = Api(app,
              title='Student Management System API',
              description=description,
              authorizations=authorizations,
              security='Bearer Auth'
              )
    
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(student_namespace, path='/student')
    

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not found"}, HTTPStatus.NOT_FOUND
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, HTTPStatus.NOT_FOUND



    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course,
            'Admin': Admin,
            'Score': Score,
            'Course': Course,
            'Student': Student,
            'Enrollment': Enrollment
        }

    return app
