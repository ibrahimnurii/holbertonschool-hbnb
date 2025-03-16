from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(
            self, first_name,  last_name, email
    ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.places = []
    
    def add_place(self, place):
        self.places.append(place)

    def to_dict(self):
        """Convert the User instance into a dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        })
        return base_dict