import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.courses import Course
from ..models.admin import Admin



class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        
        self.appctx = self.app.app_context()
        
        self.appctx.push()
        
        self.client = self.app.test_client()
        
        db.create_all()

    
    def tearDown(self):

        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_courses(self):

    # Activate the admin
        data = {
            "first_name": "Jacinda",
            "last_name": "Arden",
            "email": "jacinda@gmail.com",
            "password": "jacinda"
        }

        response = self.client.post('/admin/create_admin', json=data)

        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

    #def test_register_students(self):
        # Register a course
        reg_data = {
            "name": "Test Course",
            "teacher": "Test Teacher"
        }

        response = self.client.post('/courses', json=reg_data)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "Igneous Petrology"

        assert teacher == "Mr Shay"

         
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """def test_get_all_courses(self):
        token = create_access_token(identity="Jacinda")

        headers = {
            "Authorization": f"Bearer {token}"
        }
            
        response = self.client.post('/courses', headers=headers)

        assert response.status_code == 201

        assert response.json == []"""
    