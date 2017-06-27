from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
status=""
def index(request):
    return render(request,'login_reg/index.html')

def register(request):
    # try:
    if request.method=="POST":
        #if the fields pass the vaildation the  object will be created in the database
        #the registration methhod inside the model, performs all of the checks, creates instances if tests pass and returns True and the current user. If there is an error it will return False and errors.
        validation_response=User.objects.registration(request.POST)
        print "registration"*100, validation_response
        if validation_response[0]:
            context={
                'name': validation_response[1].name,
                'action': "registered"
            }
            request.session['current_user_id']=validation_response[1].id
            messages.success(request,'Successfully registered')
            # return render(request,'beltapp/show.html', context)
            status="loggedin"
            return redirect('travels:show')
        else:
            for error in validation_response[1]:
                messages.error(request,error)
            return redirect('auth:index')
    else:
        return redirect('auth:index')
    # except:
    #     return render(request,'login_reg/error.html')


def login(request):
    # try:
    if request.method=="POST":

        #the login methhod inside the model, performs all of the checks, returns true ,user if tests pass. If there is an error it will return False and errors.
        validation_response=User.objects.login(request.POST)
        if validation_response[0]==False:
            for error in validation_response[1]:
                messages.error(request,error)
            return redirect('auth:index')
        else:
            context={
                'name': validation_response[1].name,
                'action': "logged in"
            }
            request.session['current_user_id']=validation_response[1].id
            messages.success(request,'Successfully logged in')
            # return render(request,'beltapp/show.html', context)
            status="loggedin"
            return redirect('travels:show')
    else:
        return redirect('auth:index')
    # except:
    #     return render(request,'login_reg/error.html')

def logout(request):
    status='loggedout'
    request.session.clear()
    return redirect('auth:index')
