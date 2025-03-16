from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.extensions import db 
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenity_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auths import api as auth_ns

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object(config_class)
    
    # Initialize API, Bcrypt, JWT, and DB
    api = Api(app, version='1.0', title='HBnB API', description='HBnB application API', doc='/api/v1')
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    migrate = Migrate(app, db)
    # Register namespaces with API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auths')

    return app
