from flask_restx import fields, Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.service import facade
from app.models.users import User

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='checking is admin or not', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(400, 'Email already exists')
    @api.response(200, 'User added successfully')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user_data = api.payload

        if not facade.get_user(current_user).is_admin:
            return {'error': 'Admin privileges required'}, 403
        
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
        user: User = facade.get_user(user_id)
        if not user:
            return 'Invalid input', 400
        
        return user.to_dict(), 200  
    
    @api.expect(user_model, validate=True)
    @api.response(400, 'Invalid input')
    @api.response(200, 'User updated successfully')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user: User = facade.get_user(user_id)
        
        if not user:  
            return {'error': 'User not found'}, 404

        user_data = api.payload

        if user_id != current_user:
            return {'error': 'You cannot change a different user'}, 403

        if user_data['email'] != user.email:
            return 'You cannot modify the email.', 400

        if not user.verify_password(user_data['password']):
            return 'You cannot modify the password.', 400

        new_user = facade.update(user_id, user_data)
        return new_user.to_dict(), 200
    
    @api.response(400, 'Invalid input')
    @api.response(200, 'Deleted successfully')
    def delete(self, user_id):
        deleted_user: User = facade.delete(user_id) 
        if deleted_user:
            return {
                "message": f"Deleted user: {deleted_user.id} - {deleted_user.first_name} - {deleted_user.email}"
            }, 200
        else:
            return {"error": "User not found"}, 404
