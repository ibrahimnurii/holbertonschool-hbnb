from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name
        })
        return base_dict