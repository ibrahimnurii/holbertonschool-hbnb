from app.models.basemodel import BaseModel
from app.models.users import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner: User):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Convert the User instance into a dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict()
        })
        return base_dict