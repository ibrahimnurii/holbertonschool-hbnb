from app.extensions import db
from app.models.basemodel import BaseModel

class PlaceAmenity(BaseModel):
    __tablename__ = "place_amenity"

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), primary_key=True)
    amenity_id = db.Column(db.String(36), db.ForeignKey('amenities.id'), primary_key=True)

    def __init__(self, place_id, amenity_id):
        super().__init__()
        self.place_id = place_id
        self.amenity_id = amenity_id
