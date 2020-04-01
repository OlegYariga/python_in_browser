import datetime
from django.db import models
from django.contrib.auth.models import User, UserManager


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.description,
            'price': self.price,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }


class Student(User):
    #email = models.EmailField(default=None)
    #password = models.CharField(max_length=255, default=None)
    #first_name = models.CharField(max_length=255)
    #last_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    group = models.IntegerField()


class StudentTests(models.Model):
    tests = models.ManyToManyField('test')
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    score = models.IntegerField(default=0)


class Test(models.Model):
    module_name = models.CharField(max_length=255, default=None)
    test_name = models.CharField(max_length=255, default=None)

    def __str__(self):
        return str(self.test_name)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default=None)
    question = models.TextField(default=None)

    def __str__(self):
        return str(self.question)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    answer = models.TextField(default=None)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return str(self.answer)
