from ..utils import db

class Score(db.Model):
    __tablename__ = 'Scores'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('Students.id'), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('Courses.id'), nullable=False)
    score = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f"<{self.score}>"
        
        
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
    
