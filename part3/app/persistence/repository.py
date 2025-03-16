from abc import ABC, abstractmethod
from sqlalchemy.exc import IntegrityError
from app.extensions import db

class Repository(ABC):

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, obj):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, att_name, att_value):
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)
    
    def get_all(self):
        return self.model.query.all()
    
    def update(self, obj_id, data):
        obj = self.model.query.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return self.model.query.get(obj_id)

    def delete(self, obj_id):
        obj = self.model.query.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
        return obj
    
    def get_by_attribute(self, att_name, att_value):
        return self.model.query.filter_by(**{att_name: att_value}).first()