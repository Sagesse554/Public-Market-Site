from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from user.forms import SignUpForm, SignInForm, ChangeForm

class RegisterView(View):
    template_name = 'register.html'
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        next_url = next_url = request.GET.get('next', '')
        context = {'form': form, 'next': next_url}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            print("Account created successfully!")
            next_url = request.POST.get('next', '')
            login(request, user)
            
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')

        else:
            print("User registration failed!")
            next_url = request.POST.get('next', '')
            context = {'form': form, 'next': next_url}
            return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'login.html'
    form_class = SignInForm

    def get(self, request):
        form = self.form_class()
        next_url = request.GET.get('next', '')
        context = {'form': form, 'next': next_url}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            next_url = request.POST.get('next', '')
            user = authenticate(username=username, password=password)

            if user is not None:
                print("Login successful!")
                login(request, user)

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')
        
        else:
            print('Authentication failed!')
            next_url = request.POST.get('next', '')
            context = {'form': form, 'next': next_url}
            return render(request, self.template_name, context)


class ChangeView(PasswordChangeView):
    template_name = 'change.html'
    form_class = ChangeForm