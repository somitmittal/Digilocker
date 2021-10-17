from .api import Digilocker
from .resource.user import User
from .resource.document import Documents


class DigilockerService:

    def __init__(self, access_token):
        self.access_token = access_token
        self.user = User()
        self.documents = Documents()

    def verify_user_details(self, user_name):
        return self.user.verify_user(access_token=self.access_token, name=user_name)
