import os

# URL endpoints that are used to communicate with digilocker

# TEST_BASE_URL = "https://developers.digitallocker.gov.in/public/oauth2/1"
# TEST_ACCESS_TOKEN_URL = "https://developers.digitallocker.gov.in/public/oauth2/1/token"

# BASE URLS
BASE_URL = "https://api.digitallocker.gov.in/public/oauth2/1"
FILE_BASE_URL = "https://api.digitallocker.gov.in/public/oauth2/2"
ACCOUNT_BASE_URL = "https://api.digitallocker.gov.in/public/account/1"

# AUTH URLS
AUTH_ENDPOINT = "{}/authorize".format(BASE_URL)
ACCESS_TOKEN_URL = "{}/token".format(BASE_URL)
ACCOUNT_VERIFY = "{}/verify".format(ACCOUNT_BASE_URL)

# DOC URLS
SELF_UPLOADED_DOCS_ENDPOINT = "{}/files".format(BASE_URL)
FETCH_DOC_ENDPOINT = "{}/file".format(BASE_URL)
DOCUMENT_XML_ENDPOINT = "{}/xml".format(BASE_URL)
UPLOAD_FILE_ENDPOINT = "{}/file/upload".format(BASE_URL)
PULL_DOC_ENDPOINT = "{}/pull/pulldocument".format(BASE_URL)
ISSUER_LIST_ENDPOINT = "{}/pull/issuers".format(BASE_URL)
LIST_OF_DOCS_BY_ISSUER_ENDPOINT = "{}/pull/doctype".format(BASE_URL)
SEARCH_PARAMS_DOC_ENDPOINT = "{}/pull/parameters".format(BASE_URL)
ISSUED_DOC_LIST_ENDPOINT = "{}/files/issued".format(FILE_BASE_URL)

# USER URLS
USER_DETAILS_ENDPOINT = "{}/user".format(BASE_URL)

# DOC NAME
AADHAR_CARD = "Aadhaar Card"
PAN_CARD = "Pan Card"
DRIVING_LICENSE = "Driving License"
INSURANCE_CERTIFICATE = "Insurance Certificate"

# CUSTOMER CARE NUMBER
CUSTOMER_CARE_NUMBER = "727-727-7275"
