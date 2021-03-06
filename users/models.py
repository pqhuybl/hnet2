from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField, PhoneNumberField
from django.core.urlresolvers import reverse
from simple_history.models import HistoricalRecords
from postman.models import Message


# Create your models here.

LOCATION_CHOICES = (
    ('01', 'Rochester'),
    ('02', 'Buffalo'),
    ('03', 'New York City'),
    )

class UserProfile(models.Model):
    #history = HistoricalRecords()
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES, default='01', verbose_name='Hospital')
    user = models.OneToOneField(User, primary_key=True)
    #reference id. This id is used to hind user primary key
    ref_id = models.CharField(max_length=120, default='abc', unique=True)
    fName = models.CharField(max_length=40, verbose_name ="First Name")
    lName = models.CharField(max_length=40, verbose_name ="Last Name", )
    mName = models.CharField(max_length=40, verbose_name ="Middle Name", blank=True )
    dOB = models.DateField()
    sSN = USSocialSecurityNumberField(verbose_name ="SSN", unique=True, )
    phoneNumber = PhoneNumberField(null=True, verbose_name ="Phone")
    streetAddress = models.CharField(max_length=100, verbose_name ="Street")
    city = models.CharField(max_length=30, verbose_name ="City")
    state = USStateField(verbose_name ="State")
    zipcode = USZipCodeField(verbose_name ="Zipcode")
    email = models.EmailField(max_length=75, verbose_name ="Email", unique=True)
    dateJoin = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)



    def __str__(self):
        return self.user.username
    def get_unread_count(self):
        unread_count = Message.objects.inbox_unread_count(self.user)
        return unread_count

    '''return url for user object'''
    def get_absolute_url(self):
        #return "/users/%i/" % self.user.id
        return reverse('userprofile-detail', kwargs={'ref_id':self.ref_id})
    def get_absolute_url_update(self):
        return reverse('userprofile-update', kwargs={'ref_id':self.ref_id})
    def get_activate_url(self):
        return reverse('patient-activate', kwargs={'ref_id': self.ref_id})
    def get_discharge_url(self):
        return reverse('patient-discharge', kwargs={'ref_id': self.ref_id})
    def get_transfer_url(self):
        return reverse('patient-transfer', kwargs={'ref_id': self.ref_id})
    def get_add_doctor_url(self):
        return reverse('patient-add-doctor', kwargs={'ref_id': self.ref_id})
       
      

       
    #this is for med-info
    #get url to view user med-info
    def get_medinfo_url(self):
        return reverse('med-info-detail', kwargs={'ref_id': self.ref_id})
    #get url to init user med-info
    def get_medinfo_init_url(self):
        return reverse('med-info-init', kwargs={'ref_id': self.ref_id})
    def get_case_init_url(self):
        return reverse('case-init', kwargs={'ref_id': self.ref_id})
    def get_case_list_url(self):
        return reverse('case-list-view', kwargs={'ref_id': self.ref_id})



    #This is for staff management
    def get_employee_url(self):
        return reverse('employee-update', kwargs={'ref_id':self.ref_id})


class Employee(models.Model):
    #history = HistoricalRecords()
    employee = models.OneToOneField(User, primary_key=True, verbose_name="Employee username")
    
    EMPLOYEE_CHOICES = (
        ('D', 'Doctor'),
        ('N', 'Nurse'),
        ('R', 'Receptionist'),
        )
    #to translate, use get_employee_type_display
    employee_type = models.CharField(max_length=1, choices=EMPLOYEE_CHOICES, verbose_name="Employee Type")
    

    def __str__(self):
        return self.get_employee_type_display() + " - " + self.employee.username
    def _employee_info(self):
        info = self.get_employee_type_display() + " - " + self.employee.username + " - "+self.employee.userprofile.get_location_display()
        return info

class Doctor(models.Model):
    #history = HistoricalRecords()
    doctor = models.OneToOneField(Employee, primary_key=True, verbose_name="Doctor")
    lisence = models.CharField(max_length=10, blank=True, verbose_name="Lisence")
    specialty = models.CharField(max_length=100, default="Unknown")
    available = models.BooleanField(default=True)
    max_patients = models.PositiveSmallIntegerField(default=10,verbose_name="Max Patients")
    current_patient_count = models.PositiveSmallIntegerField(default=0, verbose_name="Current Patient Count")
    dateJoin = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return self.doctor._employee_info() + " - "+ self.specialty

    @classmethod
    def create(doc, employee):
        doctor = doc(doctor=employee)
        return doctor


class Nurse(models.Model):
    #history = HistoricalRecords()
    nurse = models.OneToOneField(Employee, primary_key=True, verbose_name="Nurse")
    available = models.BooleanField(default=True, verbose_name="Available")
    lisence = models.CharField(max_length=10, blank=True, verbose_name="Lisence")
    specialty = models.CharField(max_length=100, default="Unknown")  
    max_patients = models.PositiveSmallIntegerField(default=10,verbose_name="Max Patients")
    current_patient_count = models.PositiveSmallIntegerField(default=0, verbose_name="Current Patient Count")
    dateJoin = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
 

    @classmethod
    def create(nur, employee):
        nurse = nur(nurse=employee)
        return nurse

    def __str__(self):
        return self.nurse._employee_info() + " - " + self.specialty


class Receptionist(models.Model):

    receptionist = models.OneToOneField(Employee, primary_key=True)

    dateJoin = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
 

    @classmethod
    def create(rep, employee):
        receptionist = rep(receptionist=employee)
        return receptionist







class Patient(models.Model):
    #history = HistoricalRecords()
    patient = models.OneToOneField(User,primary_key=True, verbose_name="Patient")
    is_active = models.BooleanField(default=False)
    primary_doctor = models.ForeignKey(Doctor, verbose_name="Primary Doctor", related_name="primary_doctor", null=True)
    doctors = models.ManyToManyField(Doctor, verbose_name="Doctors", null=True)
    primary_nurse = models.ForeignKey(Nurse, verbose_name="Primary Nurse", related_name="primary_nurse", null=True)
    nurses = models.ManyToManyField(Nurse, verbose_name="Nurses", null=True)
    LAST_ACTION_CHOICES = (
        ('N', 'Joined'),
        ('A', 'Admitted'),
        ('D', 'Discharged'),
        ('T', 'Transfered'),
        ('R', 'Referred'),
        )
    last_action = models.CharField(max_length=1, choices=LAST_ACTION_CHOICES, default='N')
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    
    class Meta:
        permissions = (
            ("read_patient", "can view patient"),
            ("admit_patient", "can admit patient"),
            #to discharge patient, change is_active to false
            ("discharge_patient", "can discharge patient"),

        )
        
    def __str__(self):
        return self.patient.username
    def get_write_to_doc_url(self):
        return reverse('postman_write', kwargs={'recipients': self.primary_doctor.doctor.employee.username})
    def get_write_to_nurse_url(self):
        return reverse('postman_write', kwargs={'recipients': self.primary_nurse.nurse.employee.username})





