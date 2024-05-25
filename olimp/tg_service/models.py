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

    def __str__(self):
        return self.username


class Parents(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='parent')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    mobile_phone = PhoneField(blank=True, help_text='Contact phone number')

    class Meta:
        db_table = 'parents'

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"


class Children(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    mobile_phone = PhoneField(blank=True, help_text='Contact phone number')
    birthdate = models.DateField()
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children')

    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['surname'], name='surname_index')
        ]

    def __str__(self):
        return f"{self.surname} {self.name} {self.patronymic}"


class SubscriptionType(models.Model):
    amount_training = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'subscription_type'

    def __str__(self):
        return f"{self.amount_training}/ {self.price}"


class Employee(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    mobile_phone = PhoneField(blank=True, help_text='Contact phone number')
    job_title = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    class Meta:
        db_table = 'employee'


class TypeSport(models.Model):
    naming = models.CharField(max_length=30, primary_key=True)
    age_limitations_to = models.PositiveSmallIntegerField()
    age_limitations_after = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.naming

    class Meta:
        db_table = 'type_sport'


class Group(models.Model):
    naming = models.CharField(max_length=30)
    max_limitations_people = models.PositiveSmallIntegerField()
    age_limitations_to = models.PositiveSmallIntegerField()
    age_limitations_after = models.PositiveSmallIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    naming_sport_type = models.ForeignKey(TypeSport, on_delete=models.CASCADE,
                                          related_name='groups')

    def __str__(self):
        return self.naming

    class Meta:
        db_table = "group"


class Schedule(models.Model):
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day_of_week} {self.start_time}-{self.end_time}"

    class Meta:
        db_table = "schedule"


class GroupSchedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return f"{self.group.naming} - {self.schedule.day_of_week} {self.schedule.start_time}"

    class Meta:
        db_table = "group_schedule"


class Subscription(models.Model):
    conclusion_date = models.DateField()
    child = models.ForeignKey(Children, on_delete=models.CASCADE, related_name='subscriptions')
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, related_name='subscriptions')
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE,
                                          related_name='subscriptions')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 related_name='subscriptions')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.conclusion_date}.{self.child}.{self.group}"

    class Meta:
        db_table = 'subscription'


class Visitation(models.Model):
    date = models.DateField()
    time_of_arrival = models.TimeField()
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE,
                                     related_name='visitations')

    def __str__(self):
        return f'{self.date} {self.time_of_arrival} по абонементу {self.subscription}'

    class Meta:
        db_table = 'visitation'
