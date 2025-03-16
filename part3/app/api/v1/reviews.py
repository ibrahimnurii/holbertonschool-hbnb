from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service import facade
from app.models.places import Place
from app.models.reviews import Review

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        review_data = api.payload
        user_id = review_data.get('user_id')

        if not facade.get_user(user_id):
            return {'error': 'Invalid user'}, 400

        place_id = review_data.get('place_id')

        if not facade.get_place(place_id):
            return {'error': 'Invalid place'}, 400

        check_place: Place = facade.get_place(place_id)
        if check_place.owner_id == current_user:
            return {'error': 'You cannot review your own place.'}, 403

        checking_reviews = [
            review for review in facade.get_all_reviews() if review.user_id == current_user
        ]
        if checking_reviews:
            return {'error': 'You have already reviewed this place.'}, 400  
        
        if review_data.get('rating') < 1 or review_data.get('rating') > 5: 
            return {'error': 'Invalid rating'}, 400

        new_review = facade.add_review(review_data)
        return new_review.to_dict(), 200


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.get_all_reviews()
        if reviews:
            data = []
            for review in reviews:
                data.append(review.to_dict())
            return data, 200
        return {'error': 'List is empty'}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if review:
            return review.to_dict()
        return {'error': 'Invalid input'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        review_data = api.payload
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if current_user != user_id:
            return 'Unauthorized action.', 403

        if not facade.get_user(user_id):
           return {'error': 'Invalid owner'}, 400
        
        if not facade.get_place(place_id):
            return {'error': 'Invalid place'}, 400
        
        if not facade.get_review(review_id):
            return {'error': 'Invalid review id'}, 400
        
        new_review = facade.update_review(review_id, review_model)
        return new_review.to_dict()

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        review: Review = facade.get_review(review_id)
        if not review:
            return {'error': 'Invalid id'}, 400
        current_user = get_jwt_identity()
        if current_user != review.user.id:
            return 'Unauthorized action', 403
        
        deleted_review: Review = facade.delete_review(review_id)
        return f"deleted review:\n{deleted_review.to_dict()}"

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_all_reviews()

        reviews_data = [review for review in reviews if review.place.id == place_id]
        if reviews_data:
            data = []
            for review in reviews_data:
                data.append(review.to_dict())
            return data, 200
        
        return {'error': 'Place not found'}, 400
    
@api.route('/users/<user_id>/reviews')
class UserReviewList(Resource):
    @api.response(200, 'List of reviews for the user retrieved successfully')
    @api.response(404, 'user not found')
    def get(self, user_id):
        reviews = facade.get_all_reviews()

        reviews_data = [review for review in reviews if review.user_id == user_id]
        if reviews_data:
            data = []
            for review in reviews_data:
                data.append(review.to_dict())
            return data, 200
        
        return {'error': 'user not found'}, 404
