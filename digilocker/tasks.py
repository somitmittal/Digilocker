from celery.task import task

from digilocker.resource.document import Documents


@task
def save_user_document_list(access_token, digilocker_user_details):
    from digilocker.resource.user import User

    user_document_list = Documents().get_issued_document_list(access_token=access_token)
    digilocker_user_id = digilocker_user_details.get('digilockerid', None)

    if digilocker_user_id:
        digilocker_user_object = User().get_digilocker_user_details(digilockerid=digilocker_user_id)
        if not digilocker_user_object:
            digilocker_user_object = User().create_digilocker_user_details(user_json=digilocker_user_details)

        # digilocker_user_object may be None
        if digilocker_user_object:
            Documents().save_document_list(issued_documents=user_document_list, digilockeruser=digilocker_user_object)
