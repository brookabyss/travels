from __future__ import unicode_literals
from ..login_reg.models import User
from django.db import models
from datetime import datetime

class TripManager(models.Manager):

    def field_empty(self,postData):
        if len(postData)< 1:
            return True
        else:
            return False


    def date_check(self, postData):
     # travel dates should be future
        current_date=datetime.now()
        if postData < current_date:
            return True
        else:
            return False

    def validate_trip(self, postData,user_id):
        #check if there are any empty fields
        errors=[]

        if self.field_empty(postData['description']):
            errors.append("Description filed can't be empty")
        if self.field_empty(postData['destination']):
            errors.append("Destination filed can't be empty")
        destination=postData['destination']
        description=postData['description']

        if not self.field_empty(postData['date_from']) and (not self.field_empty(postData['date_to'])):
            date_from=datetime.strptime(postData['date_from'],'%Y-%m-%d')
            #check if travel dates are from the future
            if self.date_check(date_from):
                errors.append("'Travel Date From' has to be chosen from a future date.")
            date_to=datetime.strptime(postData['date_to'],'%Y-%m-%d')
            #check if travel dates are from the future
            if self.date_check(date_to):
                errors.append("'Travel Date To' has to be chosen from a future date.")
            #checking dates to and from
            if date_from > date_to:
                errors.append("'Travel Date To' should not be before 'Travel Date From'. ")
        else:
            errors.append("Date fileds can't be empty")
        print errors * 25

        if len(errors)<1:
            user_id=User.objects.filter(id=user_id)[0]
            if self.filter(user_id=user_id, date_from=date_from).count()>0:
                errors.append('You already have a trip booked for this date')
                return [False,errors]
            else:
                date_from=date_from.strftime("%B %d, %Y")
                date_to=date_to.strftime("%B %d, %Y")
                self.create(user_id=user_id,destination=destination,description=description,date_from=date_from, date_to=date_to)
                trips=self.all()
                return [True, trips]
        else:
            return [False,errors]



        #check if travel dates are from the future









class Trip(models.Model):
    user_id=models.ForeignKey(User, related_name="trips_id")
    destination=models.CharField(max_length=255)
    description=models.TextField(max_length=1000)
    date_from=models.CharField(max_length=255)
    date_to=models.CharField(max_length=255)
    joining_users = models.ManyToManyField(User, related_name="joined_trips", default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TripManager()
    def __str__(self):
        return self.destination
