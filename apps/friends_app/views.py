from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    return render(request, 'friends_app/index.html')

def register(request):
    check = User.objects.register(
        request.POST['name'],
        request.POST['alias'],
        request.POST['email'],
        request.POST['password'],
        request.POST['confirm'],
        request.POST['dob']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")

    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Registration Successful!!, {}".format(request.POST["name"]))
        return redirect('/')

def login(request):
    check = User.objects.login(
        request.POST['email'],
        request.POST['password']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")

    else:
        request.session["users_id"] = check["user"].id
        request.session["user_name"] = check["user"].name
        messages.add_message(request, messages.SUCCESS, "Login Successful!! Welcome, " "{}".format(check["user"].name))
        return redirect('/dashboard')

def dashboard(request):
    users = User.objects.all()
    current_user = request.session['user_name']
    current_id = request.session['users_id']
    favorites = []
    others = []
    this_user = User.objects.get(id = request.session['users_id'])
    check = False
    message = "You do not have any friends yet!"

    data = {
        'users':users,
        'current_user':current_user,
        'favorites':favorites,
        'others': others,
        'current_id': current_id,
        'check': check,
        'message': message
    }

    for x in this_user.favorites.all():
        data['favorites'].append(x)

    for x in users:
        var = True
        for y in this_user.favorites.all():
            if x.id == y.id:
                var = False
        if var == False:
            continue
        else:
            data['others'].append(x)

    if this_user.favorites.all().exists():
        data['check'] = True
        data['message'] = "You do not have any friends yet"

    


    
    return render(request, 'friends_app/dashboard.html', data)

def add_friend(request, id):
    this_user = User.objects.get(id= request.session['users_id'])
    this_friend = User.objects.get(id = id)
    this_user.favorites.add(this_friend)
    this_friend.favorites.add(this_user)

    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def view(request, id):
    this_user = User.objects.get(id=id)
    data = {
        'this_user': this_user
    }
    return render(request, 'friends_app/view.html', data)

def remove(request, id):
    this_user = User.objects.get(id=request.session['users_id'])
    removed_user = this_user.favorites.get(id=id)

    this_user.favorites.remove(removed_user)

    return redirect('/dashboard')
