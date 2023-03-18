from flask_restx import Resource, Namespace, fields
from ..models.courses import Course
from ..models.student import Student
from ..models.enrollment import Enrollment
from ..utils.decorators import admin_required
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

course_namespace = Namespace('course', description='Namespace for courses') 


course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description='Course ID'),
        'name': fields.String(description='Course Name', required=True),
        'teacher': fields.String(description='Teacher', required=True),
        'units': fields.Integer(description='Course Units', required=True )
    }
)

course_enrollment_model = course_namespace.model(
    'Enrollments', {
        'student_id': fields.Integer(description='Course ID'),
        'course_id': fields.Integer(description='Course ID')

    }
)


@course_namespace.route('')
class GetCreateCourses (Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get all courses'
    )
    @jwt_required()
    @admin_required
    def get(self):
        """
            Get all Courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK

    
   
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Register a course'
    )    
    @jwt_required()
    @admin_required
    def post(self):
        """
            Register a Course (Admin only)
        """
        data = course_namespace.payload


        course = Course.query.filter_by(name=data['name']).first()

        if course:
            return {"message": "Course Already Exists"}, HTTPStatus.CONFLICT

        new_course = Course(
            name = data['name'],
            teacher = data['teacher'],
            units = data['units']
        )

        new_course.save()

        response = {
            'id': new_course.id,
            'name': new_course.name,
            'teacher': new_course.teacher,
            'units': new_course.units
        }

        

        return response, HTTPStatus.CREATED
    

    
        
@course_namespace.route('/<int:course_id>')
class GetUpdateDelete(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Retrieve a course by ID',
        params = {
            'course_id': 'The Course  ID '
        }
    )    
    @jwt_required()
    @admin_required
    def get(self, course_id):
        """
            Retrieve a course by ID (Admin only)
        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK

    
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Update a course by ID',
        params = {
            'course_id': 'The Course ID'
        }
    )    
    @jwt_required()
    @admin_required
    def put(self, course_id):
        """
            Update a course by ID (Admin only)
        """

        course_to_update = Course.get_by_id(course_id)

        data = course_namespace.payload

        course_to_update.name = data['name']
        course_to_update.teacher = data['teacher']
        course_to_update.units = data['units']
        
        
        course_to_update.update()

        return course_to_update, HTTPStatus.OK


    @course_namespace.doc(
        description='Delete a course by ID',
        params = {
            'course_id': 'The Course ID'
        }
    )
    def delete(self, course_id):
        """
            Delete a course by ID (Admin only)
        """
        course_to_delete = Course.get_by_id(course_id)

        course_to_delete.delete()

        return {"message": "Course Deleted Successfully"}, HTTPStatus.OK



@course_namespace.route('/<int:course_id>/students')
class AllStudents(Resource):
    @jwt_required()
    @admin_required
    def get(self, course_id):
        """
            Get all students offering a course (Admin only)
        """
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, HTTPStatus.NOT_FOUND
        
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        students_list = []
        for enrollment in enrollments:
            student = Student.query.get(enrollment.student_id)
            students_list.append({
                'student_id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'registration_no': student.registration_no
            })
        return students_list, HTTPStatus.OK



@course_namespace.route('/<int:course_id>/students/<int:student_id>')
class EditCourses(Resource):
    @course_namespace.doc(
        description = "Enroll a Student for a Course (Admin only)",
        params = {
            'course_id': "The Course's ID"
        }
    )
    @jwt_required()
    @admin_required
    def post(self, course_id, student_id):
        """
            Enroll a Student for a Course (Admin only)
        """
        course = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)
        
        enrolled_student = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()
        
         # Check if student exists
        student = Student.query.filter_by(id=student_id).first()
        if not student:
            return {'message': 'Student not found'}, HTTPStatus.NOT_FOUND
        
        # Check if student is already enrolled in course
        if enrolled_student:
            return {"message": 'Student already enrolled for this course'}, HTTPStatus.OK
        
        enroll_student =  Enrollment(
            course_id = course_id,
            student_id = student_id
        )

        enroll_student.save()

        response = {
            'course_id': course_id,
            'course_name': course.name,
            'student_id': student_id,
            'student_first_name': student.first_name,
            'student_last_name': student.last_name,
            'teacher': course.teacher,
            'registration_no': student.registration_no
            
        }
        return response, HTTPStatus.CREATED
    
    
    @course_namespace.doc(
        description='Unenroll a Student from a Course',
        params = {
            'course_id': "The Course ID",
            'student_id': "The Student ID"
        }
    )
    @jwt_required()
    @admin_required
    def delete(self, course_id, student_id):
        """
            Unenroll a Student from a Course (Admin only)
        """

        student = Student.query.filter_by(id=student_id).first()
        course = Course.query.filter_by(id=course_id).first()

        if not student or not course:
            return {"message": "Student or Course Not Found"}, HTTPStatus.NOT_FOUND
        
        enrolled_student = Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first()

        enrolled_student.delete()
        
        return {"message": "Student Unenrolled Successfully"}, HTTPStatus.OK
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    