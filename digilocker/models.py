from django.db import models
from .choices import Gender


class DigilockerUserDetails(models.Model):
    """
        Digilocker Returns following user details in json format.
     digilockerid A unique 36 character DigiLocker Id of the user account.
     name The name of the user as registered with DigiLocker.
     dob This is date of birth of the user as registered with DigiLocker in DDMMYYYY
    format.
     gender This is gender of the user as registered with DigiLocker. The possible
    values are M, F, T for male, female and transgender respectively.
     eaadhaar This indicates whether eAadhaar data is available for this account.
    Possible values are Y and N.
     reference_key This is DigiLocker account reference key. This is used only as a
    transient reference for tracing.
    """

    digilockerid = models.CharField(max_length=40, db_index=True)
    name = models.CharField(max_length=40)
    dob = models.DateField(null=True)
    gender = models.CharField(choices=Gender.CHOICES, max_length=1, null=True)
    eaadhaar_available = models.BooleanField(default=False)
    reference_key = models.CharField(max_length=70, null=True)

    def __str__(self):
        return self.name


class IssuedDocsDetail(models.Model):
    digilocker_user = models.ForeignKey(DigilockerUserDetails, on_delete=models.PROTECT)
    name = models.CharField(max_length=32)
    mime = models.CharField(max_length=16, null=True)
    uri = models.CharField(max_length=64)

    def __str__(self):
        return self.name
