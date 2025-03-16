from app.persistence.repository import MemoryRepository
from app.models.users import User
from app.models.amenities import Amenity
from app.models.places import Place
from app.models.reviews import Review
class HBnBFacade:
    def __init__(self):
        self.user_repo = MemoryRepository()
        self.amenity_repo = MemoryRepository()
        self.place_repo = MemoryRepository()
        self.review_repo = MemoryRepository()

    def add_user(self, user):
        user = User(**user)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str):
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update(self, user_id: str, user: User):
        return self.user_repo.update(user_id, user)
    
    def delete(self, user_id: str):
        return self.user_repo.delete(user_id)
    
    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_attribute('email', email)
    
    def add_amenity(self, amenity):
        amenity = Amenity(**amenity)
        self.amenity_repo.add(amenity)

        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity):
        return self.amenity_repo.update(amenity_id, amenity)
    
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
    
    def add_place(self, place):
        place = Place(**place)
        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place):
        return self.place_repo.update(place_id, place)

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)
    
    def add_review(self, review):
        review = Review(**review)
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review):
        return self.review_repo.update(review_id, review)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)