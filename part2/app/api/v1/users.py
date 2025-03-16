from flask_restx import Namespace, Resource, fields
from app.service import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(400, 'Invalid input')
    @api.response(400, 'Email already exists')
    @api.response(200, 'User added successfully')
    def post(self):
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])

        if existing_user:
            return {'error': 'Email already exists'}, 400
        
        new_user = facade.add_user(user_data)
        return new_user.to_dict(), 200
    
    @api.response(400, 'List is empty')
    @api.response(200, 'List retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        if users:
            data = []
            for user in users:
                data.append(user.to_dict())
            return data, 200
        
        return 'List is empty', 400
        
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(400, 'Invalid input')
    @api.response(200, 'User retrieved successfully')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return 'Invalid input', 400
        
        return user.to_dict(), 200  
    
    @api.expect(user_model, validate=True)
    @api.response(400, 'Invalid input')
    @api.response(200, 'User updated successfully')
    def put(self, user_id):
        user_data = api.payload
        new_user = facade.update(user_id, user_data)
        return new_user.to_dict(), 200
    
    @api.response(400, 'Invalid input')
    @api.response(200, 'Deleted successfully')
    def delete(self, user_id):
        deleted_user = facade.delete(user_id)
        return f'Deleted user: {deleted_user.id} - {deleted_user.first_name} - {deleted_user.email}'
    
@api.route('/<email>')
class UserEmail(Resource):
    @api.response(400, 'Invalid Email')
    @api.response(200, 'Retrieved successfully')
    def get(self, email):
        user_by_email = facade.get_user_by_email(email)
        if not user_by_email:
            return 400, 'Invalid Email'
        
        return f'{user_by_email.id} - {user_by_email.first_name} - {user_by_email.email}'