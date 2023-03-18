import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.admin import Admin
from flask_jwt_extended import create_access_token



class AdminTestCase(unittest.TestCase):
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

    #Function to register an admin 
    def test_admin_registration(self):
            
        data = {
            "first_name": "Jacinda",
            "last_name": "Arden",
            "email": "jacinda@gmail.com",
            "password": "jacinda"
        }
        response = self.client.post('/admin/create_admin', json=data)

        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()

        assert admin.first_name == "Jacinda"

        assert admin.last_name == "Arden"

        assert response.status_code == 201

    #Function to Login an admin
    def test_admin_login(self):
        data = {
            "email": "jacinda@gmail.com",
            "password": "jacinda"
        }
        response = self.client.post('/auth/login', json=data)
        
        admin = Admin.query.filter_by(email='jacinda@gmail.com').first()
        
        assert response.status_code == 200
        
        token = create_access_token(identity=admin)

        headers = {
            "Authorization": f"Bearer {token}"
        }


    