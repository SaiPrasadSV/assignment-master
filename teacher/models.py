from django.db import models

class SubjectDetails(models.Model):
    subject_name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.subject_name

class Teacher(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    room_number = models.CharField(max_length=200, null=True)
    teacher_profile_pic = models.ImageField(default="default_profile_pic.png" ,null=True, blank=True)
    subject = models.ManyToManyField(SubjectDetails, blank=True)
    def __str__(self):
        return self.email


