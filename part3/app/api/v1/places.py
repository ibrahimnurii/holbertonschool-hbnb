from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service import facade

api = Namespace('places', description='Place description')

place_model = api.model('Place', {
    "title" : fields.String(requiered=True, description="Title of place"),
    "description" : fields.String(requiered=True, description="description of place"),
    "price" : fields.Float(requiered=True, description="price of place"),
    "latitude" : fields.Float(requiered=True, description="latitude of place"),
    "longitude" : fields.Float(requiered=True, description="longitude of place"),
    "owner_id" : fields.String(requiered=True, description="owner of place"),
    "amenities": fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(400, 'Invalid input')
    @api.response(400, 'Invalid price')
    @api.response(200, 'Place added successfully')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        place_data = api.payload
        owner_id = place_data.get('owner_id')
        amenities = place_data.get('amenities')

       
        for amenity_id in amenities:
            if not facade.get_amenity(amenity_id):
                return {'error': 'Amenity not exists'}, 400

        if owner_id != current_user:
            return {'error': 'User is not the owner'}, 403

        if not facade.get_user(owner_id):
            return {'error': 'Invalid owner'}, 400
        
        if place_data.get('price') < 0:
            return {'error': 'Invalid price'}, 400
        
        if abs(place_data.get('latitude')) > 90:
            return {'error': 'Invalid latitude'}, 400
        
        if abs(place_data.get('longitude')) > 180:
            return {'error': 'Invalid longitude'}, 400

        new_place = facade.add_place(place_data)
        return new_place.to_dict(), 200

        
    @api.response(400, 'List is empty')
    @api.response(200, 'List retrieved successfully')
    def get(self):
        places = facade.get_all_places()
        if places:
            data = []
            for place in places:
                data.append(place.to_dict())
            return data, 200
        return {'error': 'List is empty'}, 400
        
    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(404, 'Not Found')
    @api.response(200, 'place retrieved successfully')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if place:
            return place.to_dict()
                
        return {'error': 'Invalid input'}, 404
    
    @api.expect(place_model, validate=True)
    @api.response(400, 'Invalid owner')
    @api.response(400, 'Invalid id')
    @api.response(200, 'place updated successfully')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        place_data = api.payload
        owner_id = place_data.get('owner_id')

        if owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        if not facade.get_user(owner_id):
           return {'error': 'Invalid owner'}, 400
        
        if not facade.get_place(place_id):
            return {'error': 'Invalid id'}, 400
        
        new_place = facade.update_place(place_id, place_data)
        return new_place.to_dict()
    
    @api.response(400, 'Invalid input')
    @api.response(200, 'Deleted successfully')
    def delete(self, place_id):
        if not facade.get_place(place_id):
            return {'error': 'Invalid id'}, 400
        
        deleted_place = facade.delete_place(place_id)
        return deleted_place.to_dict(), 200