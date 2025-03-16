from app.models.basemodel import BaseModel
from app.extensions import db
from app.models.users import User
from app.models.places import Place

class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(155), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), unique=False, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=False, nullable=False)

    @staticmethod
    def init_relationships():
        from app.models.places import Place
        from app.models.users import User
        place = db.relationship(Place, backref="review", lazy=True)
        user = db.relationship(User, backref="review", lazy=True) 

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text= text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        from app.service import facade
        """Convert the User instance into a dictionary."""
        base_dict = super().to_dict()
        user: User = facade.get_user(self.user_id)
        place: Place = facade.get_place(self.place_id)
        base_dict.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": place.to_dict(),
            "user_id": user.to_dict()
        })
        return base_dict