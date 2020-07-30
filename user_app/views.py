from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User

from user_app import forms


def user_view(request):
    """
    The creation/conncetion form (the same view)

    Validate the form and then connect the user with "authenticate" method or
    create the new user with "create" method
    """
    context = {}
    if request.method == 'POST':
        userform = forms.UserPurBeurreForm(data=request.POST)
        if userform.is_valid():
            user = request.POST.copy()
            username = user["email"].split("@")[0]
            email = user["email"]
            password = user["password"]
            if "connexion" in request.POST:  # connection
                user = authenticate(username=username, password=password)
                if user:    # authenticated ?
                    if user.is_active:
                        login(request, user)
                        print(f"Connection of {username}")   # for the logs
                        return HttpResponseRedirect(reverse('home_app:index'))  # return to the index
                    else:
                        userform.add_error(None, "Compte désactivé : Connexion refusée")  # incactive
                else:
                    print(f"Someone try to login and failed ! user : {username} - psw : {password}")
                    userform.add_error(None, "Erreur de connexion : email/mot de passe erroné")  # connection error
            else:  # creation
                print(f"Register new user : {username} - {email}")
                new_user = User.objects.create_user(username, email, password)
                userform = forms.UserPurBeurreForm()
        else:  # form no valid
            print("Error on creation/connection form : {userform.errors}")
    else:  # not post but HTTP REQUEST
        userform = forms.UserPurBeurreForm()
    context['title'] = "Compte - Connexion/Création"
    context['userform'] = userform
    return render(request, 'user_app/layouts/userpurbeurre.html', context=context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_app:index'))
