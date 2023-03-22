import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.courses import Course
from ..models.admin import Admin
from ..models.users import User



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

         # Register a student
        data = {
            "first_name": "betty",
            "last_name": "boo",
            "email": "betty@gmail.com",
            "password": "betty",
            "registration_no": 1
        }

        response = self.client.post('/student/signup', json=data, headers=headers)


        # Register a course
        data = {
            "name": "Igneous Petrology",
            "teacher": "Mr Shay",
            "units": 3
        }

        response = self.client.post('/courses', json=data, headers=headers)

        assert response.status_code == 201

        courses = Course.query.all()

        course_id = courses[0].id

        course_name = courses[0].name

        teacher = courses[0].teacher

        assert len(courses) == 1

        assert course_id == 1

        assert course_name == "Igneous Petrology"

        assert teacher == "Mr Shay"

        

    # Retrieve all courses

        response = self.client.get('/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "name": "Igneous Petrology",
            "teacher": "Mr Shay",
            "units": 3
            }]
        
        # Update a course's details
        data = {
            "name": "Metamorphic Petrology",
            "teacher": "Mr Shay",
            "units": 3
        }

        response = self.client.put('/courses/1', json=data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 1,
            "name": "Metamorphic Petrology",
            "teacher": "Mr Shay",
            "units": 3            
        }


    # Enroll a student for a course
        response = self.client.post('/courses/1/students/2', headers=headers)

        assert response.status_code == 201

        assert response.json == {
            "course_id": 1,
            "course_name": "Metamorphic Petrology",
            "teacher": "Mr Shay",
            "student_id": 2,
            "student_first_name": "betty",
            "student_last_name": "boo",
            "registration_no": 1
        }


    # Get all students enrolled for a course
        response = self.client.get('/courses/1/students', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "student_id": 2,
            "first_name": "betty",
            "last_name": "boo",
            "registration_no": 1
        }]


    # Unenroll a student from a course
        response = self.client.delete('/courses/1/students/2', headers=headers)
        assert response.status_code == 200


        # Delete a course
        response = self.client.delete('/courses/1', headers=headers)
        assert response.status_code == 200


        