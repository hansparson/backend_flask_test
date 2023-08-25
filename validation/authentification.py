import traceback
from core.config import Config
from flask import current_app as app

class Validation(object):
    
    def __init__(self, params='', headers='', payload=''):
        self.headers = headers
        self.payload = payload
        self.params = params
        self.app = app
        
    def Authorization(self):
        try:
            authorization = False if self.headers['Authorization'] != Config.AUTHORIZATION_KEY else True
            return authorization
        except Exception:
            self.app.logger.info(traceback.format_exc())
            return False