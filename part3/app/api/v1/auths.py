from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from app.service import facade
from app.models.users import User

api = Namespace('auth', description='auth namespace')

login_model = api.model('Login',{
    'email': fields.String(required=True, description="User Email"),
    'password': fields.String(required=True, description="User Password")
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(400, 'Invalid input')
    @api.response(200, 'Access token retrieved successfully')
    def post(self):
        credentials = api.payload

        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return {'error': 'Missing email or password'}, 400

        user: User = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid input'}, 400
        access_token = create_access_token(identity=str(user.id), additional_claims={"is_admin": user.is_admin})

        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False) 

        return {
            'message': f'Hello, user {current_user}'
        }, 200