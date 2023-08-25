from flask import Blueprint, request
from services.users import UserServices

users_bp = Blueprint('user', __name__, url_prefix='/user')

@users_bp.route('/fetch', methods=['GET'])
def create_users():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    user_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = user_services.fetch_data_user()
    
    return response, response_code

@users_bp.route('/<int:id>', methods=['GET'])
def get_users_by_id(id):  # Include the "id" parameter here
    headers = request.headers
    params = request.args.to_dict()
    variables = request.view_args
    payload = request.json if request.json else {}
    
    user_services = UserServices(payload=payload, headers=headers, params=params, variables=variables)
    response, response_code = user_services.get_data_user()
    
    return response, response_code

@users_bp.route('/', methods=['GET'])
def get_all_users():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}

    user_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = user_services.get_all_user()
    
    return response, response_code

@users_bp.route('', methods=['POST'])
def add_new_user():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    print(payload)

    user_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = user_services.add_new_user()
    
    return response, response_code

@users_bp.route('', methods=['PUT'])
def update_user():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    print(payload)

    user_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = user_services.update_user_data()
    
    return response, response_code

@users_bp.route('', methods=['DELETE'])
def delete_user():
    headers = request.headers
    params = request.args.to_dict()
    payload = request.json if request.json else {}
    
    print(payload)

    user_services = UserServices(payload=payload, headers=headers, params=params)
    response, response_code = user_services.delete_user()
    
    return response, response_code