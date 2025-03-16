from flask_restx import Namespace, Resource, fields
from app.service import facade

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
    def post(self):
        review_data = api.payload
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        if not facade.get_user(user_id):
           return {'error': 'Invalid user'}, 400
        
        if not facade.get_place(place_id):
           return {'error': 'Invalid place'}, 400
        
        check_place = facade.get_place(place_id)

        if check_place.owner.id == user_id:
            return {'error' : 'You should not write review to your own place'}
       
        if review_data.get('rating') < 1 and review_data.get('rating') > 5:
           return {'error': 'Invalid rating'}, 400
        
        review_data['user'] = facade.get_user(user_id)
        review_data.pop('user_id', None)

        review_data['place'] = facade.get_place(place_id)
        review_data.pop('place_id', None)

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
    def put(self, review_id):
        place_data = api.payload
        owner_id = place_data.get('owner_id')
        place_id = place_data.get('place_id')

        if not facade.get_user(owner_id):
           return {'error': 'Invalid owner'}, 400
        
        if not facade.get_place(place_id):
            return {'error': 'Invalid id'}, 400
        
        if not facade.get_review(review_id):
            return {'error': 'Invalid review id'}, 400
        
        new_review = facade.update_review(review_id, review_model)
        return new_review.to_dict()

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        if not facade.get_review(review_id):
            return {'error': 'Invalid id'}, 400
        
        deleted_review = facade.delete_review(review_id)
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

        reviews_data = [review for review in reviews if review.user.id == user_id]
        if reviews_data:
            data = []
            for review in reviews_data:
                data.append(review.to_dict())
            return data, 200
        
        return {'error': 'user not found'}, 404
