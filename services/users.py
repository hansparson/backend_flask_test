
import traceback
import requests
from flask import current_app as app
from core.config import Config
from core.response import ErrorResponse
from core.utils import InternalError
from models.users import Users, db_users_query
from validation.authentification import Validation


class UserServices(object):
    
    def __init__(self, params='', headers='', payload='', variables=None):
        self.headers = headers
        self.payload = payload
        self.params = params
        self.variables = variables
        self.app = app
        
    def fetch_data_user(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            # Validate Param for the page
            if 'page' in self.params:
                page = self.params['page']
            else:
                raise InternalError(ErrorResponse.INVALID_PARAMETER)
            
            # Get Data From Url Fetcher
            try :
                params = {'page': page} #Optional if page Needs to be fetched
                fetch_data = requests.get(Config.FETCH_URL, params=params, timeout=2)
                if fetch_data.status_code == 200:
                    fetch_data = fetch_data.json()
                else:
                    raise InternalError(ErrorResponse.FAILED_TO_FETCH_DATA)
            except Exception:
                self.app.logger.info(traceback.format_exc())
                raise InternalError(ErrorResponse.FAILED_TO_FETCH_DATA)
            
            if not fetch_data['data']:
                raise InternalError(ErrorResponse.NO_DATA_TO_FETCH)
            
            # Save Data to Database
            failed_store = []
            succes_store = []
            for user_data_fetch in fetch_data['data']:
                user_data = dict(
                    id = user_data_fetch['id'],
                    email = user_data_fetch['email'],
                    first_name = user_data_fetch['first_name'],
                    last_name = user_data_fetch['last_name'],
                    avatar = user_data_fetch['avatar'],
                )
                store_user = Users(**user_data).save()
                if store_user == False:
                    failed_store.append(user_data)
                else:
                    succes_store.append(user_data)
            if failed_store:
                    response = ErrorResponse.DUPLICATE_ID
                    response[0]['response_data'] = {'failed_store': failed_store,
                                                    'success_Store': succes_store}
                    raise InternalError(response)
              
            self.app.logger.info("----------- SUCCESFULL SAVE DATA ORDER TO DB WITH ID {} ----------".format(store_user))
            
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Insert Data Users Successfully",
                    "response_data": {
                        "succes_store": succes_store
                    }
                }
            return response, 200
    
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
        
    def get_data_user(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            user_data = db_users_query.get_user_by_id(id=self.variables['id'])
            
            if user_data is None:
                raise InternalError(ErrorResponse.USER_NOT_FOUND)
            
            user_data = dict(
                id = user_data.id,
                email = user_data.email,
                first_name = user_data.first_name,
                last_name = user_data.last_name,
                avatar = user_data.avatar,
            )
            
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Success get data user information",
                    "response_data": user_data
                }
            return response, 200
        
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
             
    def get_all_user(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            # Validate Param for the page
            user_data = db_users_query.get_all_users()
            
            if user_data is None:
                raise InternalError(ErrorResponse.USER_NOT_FOUND)
            
            users_all = []
            for user in user_data:
                user_data = dict(
                    id = user.id,
                    email = user.email,
                    first_name = user.first_name,
                    last_name = user.last_name,
                    avatar = user.avatar,
                )
                users_all.append(user_data)
            
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Success get data user information",
                    "response_data": users_all
                }
            return response, 200
        
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
        
    def add_new_user(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            user_data = dict(
                    id = self.payload['id'],
                    email = self.payload['email'],
                    first_name = self.payload['first_name'],
                    last_name = self.payload['last_name'],
                    avatar = self.payload['avatar'],
                )
            store_user = Users(**user_data).save()
            if store_user is False:
                raise InternalError(ErrorResponse.DUPLICATE_ID)
                    
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Success added new User",
                    "response_data": user_data
                }
            return response, 200
        
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
        
    def update_user_data(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            # Querry Databases
            user_data = db_users_query.get_user_by_id(id=self.payload['id'])
            if user_data is None:
                raise InternalError(ErrorResponse.USER_NOT_FOUND)
            
            # update Database
            email = self.payload['email'] if self.payload['email'] else user_data.email
            first_name = self.payload['first_name'] if self.payload['first_name'] else user_data.first
            last_name = self.payload['last_name'] if self.payload['last_name'] else user_data.last
            avatar = self.payload['avatar'] if self.payload['avatar'] else user_data.avatar
            
            user_data = dict(
                id = user_data.id,
                email = email,
                first_name = first_name,
                last_name = last_name,
                avatar = avatar,
            )
            update_user = db_users_query.update_user_data(
                id=self.payload['id'],
                email=email,
                first_name=first_name,
                last_name=last_name,
                avatar=avatar)
            
            print(update_user)
               
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Success Update Data User for id {}".format(self.payload['id']),
                    "response_data": user_data
                }
            return response, 200
        
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
        
    def delete_user(self):
        try:
            # Check Authoization
            Authorization = Validation(
                headers=self.headers, 
                payload=self.payload, 
                params=self.params).Authorization()
            
            if Authorization is not True:
                raise InternalError(ErrorResponse.UNAUTHORIZE_ACCESS)
            
            # Querry Databases
            user_data = db_users_query.get_user_by_id(id=self.payload['id'])
            if user_data is None:
                raise InternalError(ErrorResponse.USER_NOT_FOUND)

            user_data = dict(
                id = user_data.id,
                email = user_data.email,
                first_name = user_data.first_name,
                last_name = user_data.last_name,
                avatar = user_data.avatar,
            )
            
            update_user = db_users_query.delete_user(id=self.payload['id'],status='DELETED')
            
            print(update_user)
               
            response = {
                    "response_code": "SUCCESS",
                    "response_title": "Success Delete Data User for id {}".format(self.payload['id']),
                    "response_data": user_data
                }
            return response, 200
        
        except InternalError as e:
            error_code = e.error_code
            response = error_code[0]
            code = error_code[1]
            return response, code
        
        except Exception:
            self.app.logger.info(traceback.format_exc())
            error = ErrorResponse.GENERAL_ERROR_REQUEST
            response = error[0]
            code = error[1]
            return response, code
    