from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'customuser'

    is_parent = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Parents(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    mobile_phone = PhoneField(blank=True, help_text='Contact phone number')

    class Meta:
        db_table = 'parents'


class Children(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='children')

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    mobile_phone = PhoneField(blank=True, help_text='Contact phone number')
    birthdate = models.DateField()
    parent_id = models.ForeignKey(Parents, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['surname'], name='surname_index')
        ]


class Subscriptions(models.Model):
    conclusion_date = models.DateField()
    child_id = models.ForeignKey(Children, on_delete=models.CASCADE)
    parent_id = models.ForeignKey(Parents, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subscriptions'