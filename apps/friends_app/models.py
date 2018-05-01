from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, name, alias, email, password, confirm, dob):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(alias) <2:
            errors.append("Alias must be 2 characters or more")

        if len(email) <2:
            errors.append("Email must be 2 characters or more")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) > 0:
                errors.append("Email already in use")

        if len(password)<1:
            errors.append("Password is required")
        elif len(password)<8:
            errors.append("Password must be 8 characters or more")
        if len(confirm) <1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None
        }

        if len(errors) >0:
            response["valid"] = False
            return response
        response["user"] = User.objects.create(
            name = name,
            alias = alias,
            email = email,
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
            dob = dob,
        )
        return response

    def login(self, email, password):
        errors = []

        if len(email) <1:
            errors.append("Email field cannot be empty!")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            usersMatchingEmail = User.objects.filter(email=email)
            if len(usersMatchingEmail) == 0:
                errors.append("Unknown email")

        if len(password)<1:
            errors.append("Password is required")
        elif len(password)<6:
            errors.append("Password must be 6 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "user": None,
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode(), usersMatchingEmail[0].password.encode()):
                response["user"] = usersMatchingEmail[0]
            else:
                errors.append("Incorrect Password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response





class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    dob = models.DateField()
    favorites = models.ManyToManyField('self', related_name="faves", symmetrical=False)
    
    objects = UserManager()


