from django import forms
from users.models import CustomUser
from django.core.mail import send_mail

# class UserCreateForm(forms.Form):
#     username = forms.CharField(max_length=50)
#     first_name = forms.CharField(max_length=50)
#     last_name = forms.CharField(max_length=50)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=20)

#     def save(self):
#         username = self.cleaned_data['username']
#         first_name = self.cleaned_data['first_name']
#         last_name = self.cleaned_data['last_name']
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']

#         user = CustomUser.objects.create(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#         )

#         user.set_password(password)
#         user.save()

#         return user
    

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password")

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data["password"])
        user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "picture", "first_name", "last_name", "email")
        