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
    

    def register_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
    
    # Register a student
        data = {
        "first_name": "oxla",
        "last_name": "ridd",
        "email": "tes@gmail.com",
        "password": "silenc",
        "registration_no": 14,
    }

        response = self.client.post('/student/signup', json=data, headers=headers)

        student = Student.query.filter_by(email='tes@gmail.com').first()
    

        assert student.first_name == "oxla"

        assert student.last_name == "ridd"

        assert student.email == "tes@gmail.com"

        assert student.registration_no == 14

        assert response.status_code == 201


    def retrieve_all_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
     
        # Retrieve all students
        response = self.client.get('/student', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 4,
		    "first_name": "oxla",
		    "last_name": "ridd",
		    "email": "tes@gmail.com",
		    "registration_no": 14
        }]

    
    def login_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Log a student in
        data = {
            "email":"tes@gmail.com",
            "password": "silenc"
        }

        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 201


    def retrieve_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

         # Retrieve a student's details by ID
        response = self.client.get('/student/2', headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "id": 4,
	        "first_name": "oxla",
	        "last_name": "ridd",
	        "email": "tes@gmail.com",
	        "registration_no": 14
        }

    
    def update_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Update a student's details
        data = {
            "first_name": "Mila",
            "last_name": "ridd",
            "email": "tes@gmail.com",
            "password": "silenc",
        }

        response = self.client.put('/students/2', json=data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "first_name": "Mila",
            "last_name": "ridd",
            "email": "tes@gmail.com",
            "password": "silenc",
            "registration_no": 14,
        }


    def update_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Retrieve a student's courses
        response = self.client.get('/students/4/courses', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "id": 1,
            "name": "Igneous Petrology",
            "teacher": "Mr Shay"
        }]


    def upload_score(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Upload a student's score in a course
        data = {
            "student_id": 4,
            "course_id": 1,
            "score": 80
        }

        response = self.client.post('/student/4/scores', json=data, headers=headers)

        assert response.status_code == 201

        assert response.json == {
            "student_id": 4,
            "first_name": "Mila",
            "last_name": "ridd",
            "registration_no": 14,
            "course_id": 1,
            "course_name": "Igneous Petrology",
            "teacher": "Mr Shay",
            "score": 80,
        } 

         
    def retrieve_score(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
         
         # Retrieve a student's scores
        response = self.client.get('/students/4/scores', headers=headers)

        assert response.status_code == 200

        assert response.json == [{
            "course_name": "Igneous Petrology",
            "score": 80,
            
        }]


    def update_score(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
         
        # Update a score
        data = {
            "score": 100
        }

        response = self.client.put('/student/scores/1', json=data, headers=headers)

        assert response.status_code == 200

        assert response.json == {
            "score_id": 1,
            "student_id": 4,
            "course_id": 1,
            "score": 75,
        }
    



    def delete_student(self):
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        token = create_access_token(identity=admin.id)

        headers = {
            "Authorization": f"Bearer {token}"
        }
         
    # Delete a student
        response = self.client.delete('/student/1', headers=headers)
        assert response.status_code == 200

    
   




     


