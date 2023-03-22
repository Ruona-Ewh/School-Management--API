import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.admin import Admin
from ..models.student import Student





class StudentTestCase(unittest.TestCase):
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


    def test_student(self):

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
        "registration_no": 1,
    }

        response = self.client.post('/student/signup', json=data, headers=headers)

        student = Student.query.filter_by(email='betty@gmail.com').first()
    

        assert student.first_name == "betty"

        assert student.last_name == "boo"

        assert student.email == "betty@gmail.com"

        assert student.registration_no == 1

        assert response.status_code == 201

    
    # Log a student in
        data = {
            "email":"betty@gmail.com",
            "password": "betty"
        }

        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 200

    
     # Retrieve all students
        response = self.client.get('/student', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 2,
            "first_name": "betty",
            "last_name": "boo",
            "email": "betty@gmail.com",
            "registration_no": 1
        }]

    
    # Retrieve a student's details by ID
        response = self.client.get('/student/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "betty",
            "last_name": "boo",
            "email": "betty@gmail.com",
            "registration_no": 1
        }


    # Update a student's details
        data = {
            "first_name": "betty",
            "last_name": "boop",
            "email": "betty@gmail.com",
            "password": "betty"
        }

        response = self.client.put('/student/2', json=data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 2,
            "first_name": "betty",
            "last_name": "boop",
            "email": "betty@gmail.com",
            "registration_no": 1,
        }


    # Register a course
        data = {
            "name": "Igneous Petrology",
            "teacher": "Mr Shay",
            "units": 3
        }

        response = self.client.post('/courses', json=data, headers=headers)


    #Enroll a student for a course
        response = self.client.post('/courses/1/student/2', headers=headers) 


     # Retrieve a student's courses
        response = self.client.get('/student/2/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == []


        '''# Upload a student's grade in a course
        data = {
            "student_id": 2,
            "course_id": 1,
            "score": 100.0
        }

        response = self.client.post('/student/2/scores', json=data, headers=headers)

        assert response.status_code == 404

        assert response.json == {
            "score_id": 3,
            "student_id": 2,
            "first_name": "betty",
            "last_name": "boop",
            "registration_no": 1,
            "course_id": 2,
            "course_name": "Sedimentary Petrology",
            "teacher": "Mr Boggs",
            "score": 100.0
        } '''

