# from django.db import models
from mongoengine import Document, StringField, IntField, EmailField

# Create your models here.
class Post(Document) :
    name = StringField(required=True)
    email = EmailField(required=True)
    pN = StringField(required=True)
    severity = IntField(required=True)
    description = StringField(default="No description provided.")
