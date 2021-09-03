from django.db import models
from django.contrib.auth.models import User
import uuid

class Form(models.Model):
  type_id = models.IntegerField()
  title = models.CharField(max_length=150)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  visible = models.BooleanField(default=False)

class Question(models.Model):
  description = models.TextField(max_length=500)
  forms = models.ManyToManyField(Form)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

class AnswerSheet(models.Model):
  form = models.ForeignKey(Form, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

class AnswerQuestion(models.Model):
  OPTION_TYPE = (
    ('1', 'Strongly Disagree'),
    ('2', 'Disagree'),
    ('3', 'Partially Disagree'),
    ('4', 'Neutral'),
    ('5', 'Partially Agree'),
    ('6', 'Agree'),
    ('7', 'Strongly Agree'),
  )
  option = models.CharField(max_length=25, choices=OPTION_TYPE)
  comment = models.TextField(max_length=1500, null=True, blank=True)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
  answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
  id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)