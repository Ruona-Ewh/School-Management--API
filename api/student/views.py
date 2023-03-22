from flask_restx import Namespace, Resource, fields
from ..models.student import Student
from ..models.courses import Course
from ..models.enrollment import Enrollment
from ..models.score import Score
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from ..utils.decorators import admin_required, admin_or_current_user_required
from werkzeug.security import generate_password_hash
from flask import request


student_namespace = Namespace('student', description='Namespace for student') 

signup_model = student_namespace.model(
    'Signup', {
        'first_name': fields.String(required=True, description="First Name"),
        'last_name': fields.String(required=True, description="Last Name"),
        'email': fields.String(required=True, description="Email"),
        'password': fields.String(required=True, description="Password"),
        'registration_no': fields.Integer(required=True, description="Student's Registration Number")
    }
)

student_model = student_namespace.model(
    'Student', {
        'id': fields.Integer(description="Student ID"),
        'first_name': fields.String(required=True, description=" Student's First Name"),
        'last_name': fields.String(required=True, description="Student's Last Name"),
        'email': fields.String(required=True, description="Student's Email"),
        'registration_no': fields.Integer(required=True, description="Student's Registration Number")
    }
)

student_enrollment_model =student_namespace.model(
    'Enrollments', {
        'student_id': fields.Integer(description='Student ID'),
        'course_id': fields.Integer(description='Course ID')

    }
)

score_model = student_namespace.model(
    'Score', {
    'id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'score': fields.Float(required=True),
    }
)

score_update_model = student_namespace.model(
    'ScoreUpdate', {
        'score': fields.Float(required=True, description="Students Score")       
    }
)

@student_namespace.route('/signup')
class SignUp(Resource):
    
    @student_namespace.expect(signup_model)
    @student_namespace.marshal_with(student_model)
    @jwt_required()
    @admin_required
    def post(self):
        """
            Register a student (Admin only)
        """
        data = request.get_json()

        student = Student.query.filter_by(email=data['email']).first()
        if student:
            return {"message": "Account already exists"}, HTTPStatus.CONFLICT


        new_student = Student(
            first_name = data['first_name'],
            last_name = data['last_name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            registration_no = data['registration_no']
        )

        new_student.save()

        response = {
                'id': new_student.id,
                'first_name': new_student.first_name,
                'last_name': new_student.last_name,
                'email': new_student.email,
                'registration_no': new_student.registration_no
            }

        return response, HTTPStatus.CREATED
    
    

@student_namespace.route('')
class GetStudents(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = "Retrieve All Students (Admin only)"
    )
    @jwt_required()
    @admin_required
    def get(self):
        """
            Retrieve all Students (Admin only)
        """
        students = Student.query.all()

        return students, HTTPStatus.OK


@student_namespace.route('/<int:student_id>')
class GetUpdateDeleteStudent(Resource):
    
    @student_namespace.doc(
        description = "Retrieve a Student's Details by ID",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_required
    def get(self, student_id):
        """
            Retrieve a student's Details by ID 
        """
        student = Student.get_by_id(student_id)

        response = {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'registration_no': student.registration_no
            }

        return response, HTTPStatus.OK
    
    
     
    @student_namespace.expect(signup_model)
    @student_namespace.doc(
        description = "Update a Student's Details by ID",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_or_current_user_required
    def put(self, student_id):
        """
            Update a Student's information by ID (Admin only or Student)
        """
        student = Student.get_by_id(student_id)
            
        data = student_namespace.payload

        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.email = data['email']
        student.password_hash = generate_password_hash(data['password'])

        student.update()

        response = {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'email': student.email,
                'registration_no': student.registration_no,
            }
        
        return response, HTTPStatus.OK
    
    
    
    @student_namespace.doc(
        description = 'Delete a Student by ID',
        params = {
            'student_id': "The Student's ID"
        }
    )

    @jwt_required()
    @admin_required
    def delete(self, student_id):
        """
            Delete a student by ID (Admin only)
        """
        student_to_delete = Student.get_by_id(student_id)

        student_to_delete.delete()

        return {"message": "Student Deleted Successfully"}, HTTPStatus.OK
    


@student_namespace.route('/<int:student_id>/courses')
class GetAllStudentCourses(Resource):

    @student_namespace.doc(
        description = "Retrieve a Student's Courses",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_or_current_user_required
    def get(self, student_id):
        """
            Retrieve a Student's Courses (Admin Only or User)
        """
            
        enrollments = Enrollment.get_courses_by_student(student_id)
        #.query.filter_by(student_id=course_id).all()
        course_list = []
        
        for enrollment in enrollments:
            course = Course.query.get(enrollment.id)
            course_list.append({
                'id': course.id,
                'name': course.name,
                'teacher': course.teacher,
                'units': course.units
            })

            
        return course_list, HTTPStatus.OK
    




@student_namespace.route('/<int:student_id>/scores')
class GetAddUploadScore(Resource):

    @student_namespace.doc(
        description = "Retrieve a Student's Score",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_or_current_user_required
    def get(self, student_id):
        """
            Retrieve a Student's Score (Admin Only or Student)
        """

        student = Student.get_by_id(student_id)
        if not student:
           return {"message": "Student Not Found"}, HTTPStatus.NOT_FOUND
                   
        
        
        grade_list = []

        for course in student.courses:
            grade = Score.query.filter_by(student_id=student_id, course_id=course.id).first()
            if grade:
                grade_list.append({
                    'course_name': course.name,
                    'course_id': course.id,
                    'score': grade.score
                })
                

            
        return grade_list, HTTPStatus.OK
    
    
    
    @student_namespace.expect(score_model)
    @student_namespace.doc(
        description = "Upload a Student's Score in a Course (Admin only)",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_required
    def post(self, student_id):
        """
            Upload a Student's Score in a Course (Admin only)
        """
        data = student_namespace.payload

        student = Student.get_by_id(student_id)
        course = Course.get_by_id(id=data['course_id'])

        
        # Confirm that the student is offering the course
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course.id).first()
        if not enrollment:
            return {"message": "Student is not offering the course"}, HTTPStatus.NOT_FOUND
        
        # Upload  a new score
        new_score = Score(
            student_id = student_id,
            course_id = data['course_id'],
            score = data['score'],
        )

        new_score.save()

        response = {
            'course_name': course.name,
            'teacher': course.teacher,
            'score_id': new_score.id,
            'score': new_score.score,
            'student_id': new_score.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'registration_no': student.registration_no,
            'course_id': new_score.course_id
        }

        return response, HTTPStatus.CREATED


@student_namespace.route('/scores/<int:score_id>')
class UpdateScore(Resource):

    @student_namespace.expect(score_update_model)
    @student_namespace.doc(
        description = "Update a Score (Admin Only)",
        params = {
            'score_id': "The Grade's ID"
        }
    )
    @jwt_required()
    @admin_required
    def put(self, score_id):
        """
            Update a Score (Admin Only)
        """
        data = student_namespace.payload

        score_update = Score.get_by_id(score_id)
        
        score_update.score = data['score']
        
        score_update.update()

        response = {
            'score_id': score_update.id,
            'score': score_update.score,
            'student_id': score_update.student_id,
            'course_id': score_update.course_id
        }

        return response, HTTPStatus.OK
    


@student_namespace.route('/<int:student_id>/gpa')
class GetStudentGPA(Resource):

    @student_namespace.doc(
        description = "Calculate a Student's GPA (Admin only)",
        params = {
            'student_id': "The Student's ID"
        }
    )
    @jwt_required()
    @admin_or_current_user_required
    def get(self, student_id):
        """
            Calculate a Student's GPA (Admin or current user only)
        """
         #Verify that the student exists
        student = Student.query.get(student_id)

        if not student:
            return {"message": "Student not found"}, HTTPStatus.NOT_FOUND
        
        student_scores = Score.query.filter_by(student_id=student_id).all()
        total_units = 0
        total_points = 0
        
        for score in student_scores:
            course = Course.query.get(score.course_id)
            total_units += course.units
            total_points += (4.0 * score.score / 100) * course.units
        
        gpa = round(total_points / total_units, 2) if total_units != 0 else 0.0
        
        student = Student.query.get(student_id)
        student.gpa = gpa


        
        return {"message": f" The Student's GPA is {gpa}"}, HTTPStatus.OK
        
        
        
        

        
            