from digilocker.connection import Connection
from digilocker.constants import ISSUED_DOC_LIST_ENDPOINT, FETCH_DOC_ENDPOINT, DOCUMENT_XML_ENDPOINT
from digilocker.models import IssuedDocsDetail


class Documents(object):
    def __init__(self):
        self.connection = Connection()

    def get_issued_document_list(self, access_token):
        headers = {
            "Authorization": "Bearer {0}".format(access_token)
        }
        issued_documents = self.connection.make_request(ISSUED_DOC_LIST_ENDPOINT, "GET", headers=headers)
        issued_documents = issued_documents.json()
        return issued_documents

    def get_uploaded_document(self):
        pass

    def get_document(self, access_token, uri, xml_format=False, save_document=False):
        headers = {
            "Authorization": "Bearer {0}".format(access_token)
        }
        # calling the digilocker get documents api
        if xml_format:
            response = self.connection.make_request("{}/{}".format(DOCUMENT_XML_ENDPOINT, uri), "GET", headers=headers)
            return response
        else:
            document = self.connection.make_request("{}/{}".format(FETCH_DOC_ENDPOINT, uri), "GET", headers=headers)
            if save_document is True:
                self.save_document(document)
            return document

    def save_document(self, document):
        document_data = document.content
        document_name = document.headers.get('filename')
        content_type = document.headers.get('content-type')
        start_index = content_type.find("/")
        document_extension = content_type[start_index + 1:]

        filename = document_name + "." + document_extension
        with open(filename, "wb") as f:
            f.write(document_data)

    def save_document_list(self, issued_documents, digilockeruser):
        issued_documents_list = issued_documents.get('items', [])
        """
        {'items': [{'name': 'Aadhaar Card', 'type': 'file', 'size': '',
                     'date': '26-07-2021', 'parent': '',
                     'mime': ['application/pdf'],
                     'uri': 'in.gov.uidai-ADHAR-xxxxxxxxxx',
                     'doctype': 'ADHAR', 'description': 'Aadhaar Card',
                     'issuerid': 'in.gov.uidai',
                     'issuer': 'Aadhaar, Unique Identification Authority of India'}],
                     'resource': 'R'}
        """
        for document in issued_documents_list:
            name = document.get('name')
            uri = document.get('uri')
            mime = document.get('mime')[0]
            IssuedDocsDetail.objects.create(name=name, uri=uri, mime=mime, digilocker_user=digilockeruser)

    @staticmethod
    def get_document_details(digilocker_user_id, doc_name=None):
        document_details = IssuedDocsDetail.objects.filter(digilocker_user__digilockerid=digilocker_user_id)
        if doc_name:
            document_details = document_details.filter(name=doc_name)

        return document_details
