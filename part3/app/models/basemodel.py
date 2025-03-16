from datetime import datetime
from app.extensions import db
from datetime import timezone
import uuid

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key =True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert the BaseModel instance into a dictionary."""

        return {
            "id": self.id
        }