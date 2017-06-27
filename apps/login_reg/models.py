from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.db import models
from datetime import datetime, timedelta
from django.contrib import messages
import re
import bcrypt



class UserManager(models.Manager):
    def field_empty(self,postData):
        if len(postData)< 1:
            return True
        else:
            return False

    def check_length(self,postData):
        if len(postData) < 3:
            return True
        else:
            return False

    # def check_email(self,postData):
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    #     if not EMAIL_REGEX.match(postData):
    #         return True
    #     else:
    #         return False
    def check_password_length(self,password):
        if len(password) <8:
                return True
        else:
                return False
    def confirm_password (self,password,c_password):
        if password!=c_password:
                return True
        else:
                return False

    # def birthday_check(self, birthday):
    #     # you have to be at least a day old to register
    #     current_date=datetime.now()-timedelta(days=1)
    #     print "Date time now", datetime.now()
    #     print"Current date #$^$%^$%^", current_date
    #     if birthday > current_date:
    #         return True
    #     else:
    #         return False



    def registration(self,postData):
        name=postData['name']
        user_name=postData['user_name']
        # email=postData['email']
        password=postData['password']
        c_password=postData['confirm']
        errors=[]
        #check if there are any empty fields
        for field in postData:
            if self.field_empty(field):
                errors.append("Fields can't be empty")
                break
        #strip date

        # if not self.field_empty(postData['birthday']):
        #     birthday=datetime.strptime(postData['birthday'],'%Y-%m-%d')
        #     # print "HELooooooooo"*100
        #     if self.birthday_check(birthday):
        #
        #         errors.append("You have to be at least a day old to register")
        #     # print "Messages"*10,messages
        # else:
        #     # print "Broooook"*20,not self.field_empty(postData['birthday'])
        #     errors.append("You have to be at least a day old to register")

        #check for name
        if self.check_length(name):
            errors.append("The length of name can't be less than three charcters.")
        #check for user_name
        if self.check_length(user_name):
            errors.append("The length of user name can't be less than three charcters.")
        #check email
        # if self.check_email(email):
        #     errors.append("Email invalid format")
        # Check password
        if self.check_password_length(password):
            errors.append("Password too short!")
        if self.confirm_password(password,c_password):
            errors.append("Passwords don't match")
        # if self.filter(email=email).count()>0:
        #     errors.append('Email address already exists')
        if self.filter(user_name=user_name).count()>0:
            errors.append('Please try another user name, that one is taken.')

        if len(errors)<1:
            hashed_pw=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.create(name=name,user_name=user_name,password=hashed_pw)
            user=self.filter(user_name=user_name)[0]
            return [True,user]
        else:
            return [False,errors]



    def login(self,postData):
        # email=postData['email']
        user_name=postData['user_name']
        password=postData['password']
        users=self.filter(user_name=user_name)
        errors=[]
        if users.count()< 1:

            errors.append("Username or password is incorrect")
            return [False,errors]
        else:

            for user in users:
                print"Try password"*20
                if bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8'))==user.password.encode('utf-8'):
                    return [True,user]
                else:
                    errors.append("Username or password is incorrect")
            return [False,errors]



class User(models.Model):
    name=models.CharField(max_length=255)
    user_name=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
    def __str__(self):
        return self.name
