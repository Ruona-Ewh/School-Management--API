from .users import User
from ..utils import db

class Admin(User):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer(), db.ForeignKey('Users.id'), primary_key=True)

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