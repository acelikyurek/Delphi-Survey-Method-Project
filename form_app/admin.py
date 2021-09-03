from django.contrib import admin
from .models import Form, Question, AnswerSheet, AnswerQuestion

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(AnswerSheet)
admin.site.register(AnswerQuestion)