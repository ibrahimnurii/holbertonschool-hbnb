
from app.models.basemodel import BaseModel
from app.extensions import db
import app

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @staticmethod
    def init_relationships():
        from app.models.places import Place
        from app.models.reviews import Review
        place = db.relationship(Place, backref="user", lazy=True)
        review = db.relationship(Review, backref="user", lazy=True)
    
    def __init__(self, first_name, last_name, email, password, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        return app.bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return app.bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert the User instance into a dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return base_dict
