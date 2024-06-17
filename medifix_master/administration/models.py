from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import uuid

type_of_camp = (
    ("Paid","Paid"),
    ("Free","Free"),
)

def no_future_date_validator(value):
    if value > timezone.now().date():
        raise ValidationError('Future dates are not allowed')
    
class profile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    camp_register = models.BooleanField(default=False)
    submitted_application = models.BooleanField(default=False)
    about = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.user_name.username
    
class camp_details(models.Model):
    camp_name = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    contact_website = models.URLField(max_length=200, null=True, blank=True)
    hospital_name = models.CharField(max_length=150,null=True, blank=True)
    club_name = models.CharField(max_length=150,null=True, blank=True)
    other = models.CharField(max_length = 150, null=True, blank=True)
    description = models.TextField(max_length = 3000, null=True)
    type_of_camp = models.CharField(max_length=30, null=True, choices=type_of_camp)
    cost = models.IntegerField(null=True, blank=True, default='0')
    total_camp_registrations = models.IntegerField()
    camp_register_active = models.BooleanField(default=False)
    registration = models.BooleanField(default=False)
    createdby = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)


    def __str__(self):
        return self.camp_name
    
    def clean(self):
        super().clean()
        if not (self.hospital_name or self.club_name or self.other):
            raise ValidationError("At least one of the fields Hospital Name or Club Name or Other must be filled.")
        
        if self.type_of_camp == "Paid" and not self.cost:
            raise ValidationError("Cost field is mandatory for paid camps.")
        elif self.type_of_camp == "Free" and self.cost is not None:
            raise ValidationError("Cost field should not be filled for free camps.")
        
        if self.registration and (not self.start_date_time or not self.end_date_time):
            raise ValidationError("Start Date Time and End Date Time must be provided for registered camps.")
        
        if self.camp_register_active and (not self.start_date_time or not self.end_date_time):
            raise ValidationError("Start Date Time and End Date Time must be provided for registered camps.")
        
class camp_services(models.Model):
    camp_name = models.ForeignKey(camp_details, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.camp_name.camp_name} - {self.service_name}"
    
class doctor(models.Model):
    camp_name = models.ForeignKey(camp_details, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255, null=True)
    doctor_title = models.CharField(max_length=255, null=True)
    doctor_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.doctor_name
    
class appointment(models.Model):
    appointment_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    camp_name = models.ForeignKey(camp_details, on_delete=models.DO_NOTHING, null=True)
    token_no = models.IntegerField(null=True)
    appointment_date = models.DateField()

    def __str__(self):
        return f"{self.user_name.username} - {self.camp_name.camp_name}"