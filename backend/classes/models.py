from django.db import models
from django.contrib.auth.models import User

class educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Class(models.Model):
    name = models.CharField(max_length=255)
    educator = models.ForeignKey(educator, on_delete=models.CASCADE)
    students = models.ManyToManyField(student, through='ClassMembership')
    classTime = models.DateTimeField()
    description = models.TextField()
    syllabus = models.TextField()

class ClassMembership(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)