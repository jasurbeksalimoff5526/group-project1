from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email"]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ism'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Familiya'}),
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'elektron pochta'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Parol'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Parolni tasdiqlang'
        })

        self.fields['password1'].label = "Parol"
        self.fields['password2'].label = "Parolni tasdiqlang"


    def clean(self):
        cleaned_data = super().clean()

        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")
        f_name = cleaned_data.get("first_name")
        l_name = cleaned_data.get("last_name")


        if p1:
            p1_lower = p1.lower()

            if username and username.lower() in p1_lower:
                self.add_error("password1", "Parol username-ga o'xshamasin!")
            
            if f_name and f_name.lower() in p1_lower:
                self.add_error("password1", "Parol ismga o'xshamasin!")
    
            if l_name and l_name.lower() in p1_lower:
                self.add_error("password1", "Parol familiyaga o'xshamasin!")

        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu foydalanuvchi nomi band. Boshqa nom tanlang.")

        forbidden_usernames = ['admin', 'root', 'superuser', 'moderator']
        if username.lower() in forbidden_usernames:
            raise forms.ValidationError("Bu nomdan foydalanish taqiqlangan.")
        
            
        return username
    
    def clean_first_name(self):

        f_name = self.cleaned_data.get("first_name")
        if len(f_name) < 3:
            raise forms.ValidationError("Ism kamida 3ta elementdan iborat bolishi shart")
        
        if not f_name.isalpha():
            raise forms.ValidationError("Ism faqat harfdan iborat bo'lsin")
        
        return f_name
    
    def clean_last_name(self):
        l_name = self.cleaned_data.get("last_name")
        if len(l_name) < 3:
            raise forms.ValidationError("Familiya kamida 3ta elementdan iborat bolishi shart")
        
        if not l_name.isalpha():
            raise forms.ValidationError ("Familiya faqat harfdan iborat bo'lsin")
        
        return l_name
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if len(email) < 12:
            raise forms.ValidationError("Email kamida 12 ta elementdan iborat bo'lishi kerak")
        
        return email
        

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username kiriting'
        }),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Parol'
        }),
        label="Parol"
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar', 'bio']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name.isalpha():
            raise forms.ValidationError("Ism faqat harflardan iborat bo'lishi kerak 🔠")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.isalpha():
            raise forms.ValidationError("Familiya faqat harflardan iborat bo'lsini 🔠")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        
        if CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon boshqa foydalanuvchi tomonidan band qilingan 📧")
        return email
