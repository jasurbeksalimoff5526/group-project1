from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import SignupForm, LoginForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

class SignUpView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'auth/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1') 
            user.set_password(raw_password)
            user.save()
            login(request, user) 
            return redirect('home')
        return render(request, 'auth/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "auth/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Email yoki parol noto'g'ri!")
                
        return render(request, "auth/login.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "profile.html", {"user_profile": request.user})
    

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'profile_update.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=request.user.id) 
        
        return render(request, 'profile_update.html', {'form': form})
    

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'auth/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # MUHIM: Parol o'zgargandan keyin foydalanuvchi sessiyasi yopilib qolmasligi uchun
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz muvaffaqiyatli o'zgartirildi! ✅")
            return redirect('profile', id=user.id)
        
        return render(request, 'auth/change_password.html', {'form': form})


def logout_view(request):
    logout(request) # Foydalanuvchi sessiyasini o'chiradi
    return redirect('login') # Chiqib bo'lgach login sahifasiga yuboradi