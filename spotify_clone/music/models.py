from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os


class ApiKey(models.Model):
    user = models.ForeignKey(User, related_name="api_keys", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    encrypted_api_key = models.BinaryField(null=True, blank=True)

    @property
    def key(self) -> str:
        cipher_suite = Fernet(os.environ["ENCRYPTION_KEY"])
        return (
            cipher_suite.decrypt(self.encrypted_api_key).decode()
            if self.encrypted_api_key
            else ""
        )

    @key.setter
    def key(self, value) -> None:
        cipher_suite = Fernet(os.environ["ENCRYPTION_KEY"])
        self.encrypted_api_key = cipher_suite.encrypt(value.encode())


# Create your models here.
