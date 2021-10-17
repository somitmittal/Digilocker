from datetime import datetime

from ..choices import Gender
from .document import Documents
from ..connection import Connection
from ..constants import USER_DETAILS_ENDPOINT, CUSTOMER_CARE_NUMBER
from ..models import DigilockerUserDetails
from ..tasks import save_user_document_list
from spinny.common.logger import Logger

logger = Logger.get_logger('Digilocker_User')


class User:
    def __init__(self):
        self.connection = Connection()

    def get_user_details(self, access_token):
        headers = {
            "Authorization": "Bearer {0}".format(access_token)
        }
        response = self.connection.make_request(USER_DETAILS_ENDPOINT, "GET", headers=headers)
        response_json = response.json()
        self.save_user_details(user_json=response_json)
        return response_json

    @staticmethod
    def set_eaadhaar(user_json):
        eaadhaar = user_json.get('eaadhaar', None)
        if eaadhaar == 'Y':
            user_json['eaadhaar'] = True
        else:
            user_json['eaadhaar'] = False

    @staticmethod
    def parse_dob(user_json):
        dob = user_json.get('dob', None)
        # dob can be empty string here ''
        if dob:
            try:
                dob = datetime.strptime(dob, "%d%m%Y").date()
            except ValueError as e:
                logger.error("Wrong date format received from digilocker for dob. Expected format DDMMYYYY")
                dob = None
        else:
            dob = None
        user_json['dob'] = dob

    @staticmethod
    def set_gender(user_json):
        gender = user_json.get('gender', None)
        # gender can be an empty string ''
        if gender:
            if gender not in Gender.valid_gender_choices:
                gender = None
        else:
            gender = None
        user_json['gender'] = gender

    def preprocess_user_json(self, user_json):
        self.set_eaadhaar(user_json)
        self.parse_dob(user_json)
        self.set_gender(user_json)
        return user_json

    def save_user_details(self, user_json):
        digilockerid = user_json.get('digilockerid', None)

        if digilockerid is not None:
            if self.get_digilocker_user_details(digilockerid) is None:
                digilocker_user_object = self.create_digilocker_user_details(user_json=user_json)

    def verify_user(self, access_token, name):
        user_details_json = self.get_user_details(access_token=access_token)
        user_name = user_details_json.get('name', None)
        digilocker_user_id = user_details_json.get('digilockerid', None)

        if digilocker_user_id:
            if not Documents().get_document_details(digilocker_user_id=digilocker_user_id):
                save_user_document_list(access_token=access_token, digilocker_user_details=user_details_json)

        if not user_name or not name:
            return False, "Verification Failed, Name does not exist for User"

        name = name.lower()
        user_name = user_name.lower()

        if user_name != name:
            return False, "ERROR - Aadhaar details don't match with details provided by you. " \
                          "Please connect with our Sales Executive at {} for further clarification"\
                .format(CUSTOMER_CARE_NUMBER)
        return True, "User Successfully Verified"

    @staticmethod
    def get_digilocker_user_details(digilockerid):
        try:
            return DigilockerUserDetails.objects.get(digilockerid=digilockerid)
        except DigilockerUserDetails.DoesNotExist:
            return None

    def create_digilocker_user_details(self, user_json):
        """
        Sample Output from Digilocker
        {
        "digilockerid": "123e4567-e89b-12d3-a456-426655440000",
        "name": "Sunil Kumar",
        "dob": "31121970",(DDMMYYYY) -> preprocessed to Date Object
        "gender": "M",
        "eaadhaar": "Y", -> preprocessed to Boolean Value
        "reference_key":
        "2a33349e7e606a8ad2e30e3c84521f9377450cf09083e162e0a9b1480ce0f972"
        }
        """

        user_details = self.preprocess_user_json(user_json=user_json)
        digilockerid = user_details['digilockerid']
        name = user_details['name']
        dob = user_details['dob']
        gender = user_details['gender']
        eaadhaar_available = user_details['eaadhaar']
        reference_key = user_details['reference_key']
        # name can be an empty string ''
        if digilockerid and name:
            return DigilockerUserDetails.objects.create(digilockerid=digilockerid, name=name, dob=dob, gender=gender,
                                                        eaadhaar_available=eaadhaar_available, reference_key=reference_key)
        return None
