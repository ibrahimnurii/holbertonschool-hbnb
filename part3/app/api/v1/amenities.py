from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service import facade

api = Namespace('amenity', description='Amenity description')

amenity_model = api.model("Amenity",{
    "name": fields.String(required=True, description="Name of amenity")
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(400, "Invalid Input")
    @api.response(200, "Added successfully")
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        amenity_data = api.payload

        if not user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        new_amenity = facade.add_amenity(amenity_data)
        return new_amenity.to_dict(), 200

    @api.response(400, "List is empty")
    @api.response(200, "Retrieved successfully")
    def get(self):
        amenities = facade.get_all_amenities()
        if amenities:
            data = []
            for amenity in amenities:
                data.append(amenity.to_dict())
            return data, 200
        return { "error": "List is empty" }, 400

@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(400, "Invalid id")
    @api.response(200, "Retrieved successfully")
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        
        return {"error": "Invalid input"}, 400
    
    @api.expect(amenity_model)
    @api.response(400, "Invalid input")
    @api.response(200, "Updated successfully")
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        if not user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            updated_data = facade.update_amenity(amenity_id, amenity_data)
            return updated_data.to_dict(), 200
        
        return {"error": "Invalid input"}, 400

    @api.response(400, "Invalid input")
    @api.response(200, "Updated successfully")
    def delete(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            deleted_data = facade.delete_amenity(amenity_id)
            return deleted_data.to_dict(), 200
        
        return {"error": "Invalid input"}, 400
