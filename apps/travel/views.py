from django.shortcuts import render, redirect, reverse
from ..login_reg.models import User
from .models import Trip
from django.contrib import messages

def show(request):
    current_user=request.session["current_user_id"]
    user=User.objects.filter(id=current_user)[0]
    trips=Trip.objects.filter(user_id=user )| Trip.objects.filter(joining_users=user)
    travels=Trip.objects.exclude(user_id=user)
    context={
        'user': user,
        'trips': trips,
        'travels':travels
    }
    return render(request,'travel/show.html', context)


def add(request):
    return render(request,'travel/new.html')

def create(request):
    # return [False,errors]
    user_id=request.session['current_user_id']
    validation_repsonse=Trip.objects.validate_trip(request.POST,user_id)
    if validation_repsonse[0]==True:
        return redirect(reverse('travels:show'))
    else:
        for error in validation_repsonse[1]:
            messages.error(request,error)
        return redirect(reverse('travels:add'))

def join(request,trip_id):
    print trip_id *25
    trip=Trip.objects.filter(id=trip_id)[0]
    current_user=request.session["current_user_id"]
    user=User.objects.filter(id=current_user)[0]
    trip.joining_users.add(user)
    return redirect(reverse('travels:show'))

def destination(request,t_id):
    current_user=request.session["current_user_id"]
    user=User.objects.filter(id=current_user)[0]
    trip=Trip.objects.filter(id=t_id)[0]
    joining=trip.joining_users.all()
    context={
        "trip": trip,
        "joining": joining
    }
    return render(request,'travel/destination.html', context)
