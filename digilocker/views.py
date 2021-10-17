from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from urllib.parse import urlencode

from digilocker.api import Digilocker
from digilocker.config import DIGILOCKER_CLIENT_ID, DIGILOCKER_CLIENT_SECRET, DIGILOCKER_REDIRECT_URI
from digilocker.service import DigilockerService
from spinny.common.logger import Logger

digilocker_api = Digilocker(DIGILOCKER_CLIENT_ID, DIGILOCKER_CLIENT_SECRET, DIGILOCKER_REDIRECT_URI)
logger = Logger.get_logger("Digilocker Views")


class DigilockerAuthView(APIView):

    authentication_classes = []
    throttle_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_name = request.data.get('name', None)
        user_mobile_number = request.data.get('mobile_number', None)

        auth_url = digilocker_api.get_authorization_url(mobile_number=user_mobile_number, state=request.data)
        return Response({'Auth URL': auth_url}, status=HTTP_200_OK)


class DigilockerVerifyUserView(APIView):

    authentication_classes = []
    throttle_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code', None)
        state_data = request.query_params.get('state', None)
        redirect_url = request.query_params.get('redirect_url', None)

        try:
            # state_data=name=name of user (this is how state data looks like)
            user_name = state_data.split('=')[1].replace('+', ' ')
        except Exception as e:
            user_name = None
            logger.error("Error in parsing State Data {} ".format(state_data))

        if not code:
            return Response({"error": "Digilocker Authorization failed"}, status=HTTP_401_UNAUTHORIZED)
        if not user_name:
            return Response({"error": "Verification Failed, Name of User not Found"}, status=HTTP_400_BAD_REQUEST)
        if not redirect_url:
            return Response({"error": "Verification Failed, Redirect URL not Found"}, status=HTTP_400_BAD_REQUEST)

        access_token_json = digilocker_api.get_access_token(code)
        access_token = access_token_json.get('access_token', None)

        if not access_token:
            return Response({"error": "Error in fetching Digilocker Access Token"},
                            status=HTTP_404_NOT_FOUND)

        digilocker_service = DigilockerService(access_token=access_token)
        ok, message = digilocker_service.verify_user_details(user_name)
        query_string = urlencode({'ok': ok, 'message': message})
        redirect_url = '{}?{}'.format(redirect_url, query_string)
        return redirect(to=redirect_url)
