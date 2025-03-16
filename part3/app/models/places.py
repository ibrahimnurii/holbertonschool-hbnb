from app.models.basemodel import BaseModel
from app.extensions import db
from app.models.users import User


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(55), nullable=False)
    description = db.Column(db.String(55), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=False, nullable=False)

    @staticmethod
    def init_relationships():
        from app.models.reviews import Review
        from app.models.users import User
        from app.models.amenities import Amenity
        from app.models.place_amenity import PlaceAmenity
        owner = db.relationship(User, backref="place", lazy=True)
        review = db.relationship(Review, backref="place", lazy=True)
        amenities = db.relationship(Amenity, secondary=PlaceAmenity, backref=db.backref('place', lazy=True), lazy=True)
    

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        
    def to_dict(self):
        from app.service import facade
        """Convert the Place instance into a dictionary."""
        base_dict = super().to_dict()
        facade_id = self.owner_id
        owner: User = facade.get_user(facade_id)
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": owner.to_dict()
        })
        return base_dict
