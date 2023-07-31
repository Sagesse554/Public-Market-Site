from django.shortcuts import render, redirect
from django.contrib.auth import logout


def IndexView(request):

    print('On the dashboard!')
    return render(request, 'index.html')


def LogoutView(request):
    
    logout(request)
    print('Successfully disconnected!')
    return redirect('home')