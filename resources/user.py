from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Cannot be blank!')
    parser.add_argument('password', type=str, required=True, help='Cannot be blank!')

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists!'}

        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {'message': 'An error occurred while creating an uesr!'}
        
        return {'message': 'User created!'}