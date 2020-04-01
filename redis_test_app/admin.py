from django.contrib import admin
from .models import Student, Answer, Question, Test, StudentTests


admin.site.register(Student)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(StudentTests)
