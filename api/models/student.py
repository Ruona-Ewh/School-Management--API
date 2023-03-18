from ..utils import db
from .users import User

class Student(User):
    __tablename__ = 'Students'
    id = db.Column(db.Integer(), db.ForeignKey('Users.id'), primary_key=True)
    registration_no = db.Column(db.Integer(), unique=True)
    courses = db.relationship('Course', secondary='Enrollment', lazy=True)
    score = db.relationship('Score', backref='student_score', lazy=True)
    

    def __repr__(self):
        return f"<{self.registration_no}>"

    def save(self):
        db.session.add(self)
        db.session.commit()        
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    
