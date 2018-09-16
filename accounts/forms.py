from django import forms
from django.contrib.auth import (
   authenticate,
   get_user_model,
   login,
   logout
)
from dal import autocomplete
from posts.models import Country, UserPhone

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label=" Email address")
    email2 = forms.EmailField(label="Confirm Email")
    password = forms.CharField(widget=forms.PasswordInput)
    country = forms.ModelChoiceField(
         queryset=Country.objects.all(),
         widget=autocomplete.ModelSelect2(url='/country-autocomplete')
         )
    birth_date = forms.DateField(widget=forms.TextInput(
        attrs={'type': 'date'}
    ))

    class Meta:
        model = User
        fields = ['email', 'email2', 'password', 'country', 'birth_date']

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError('Emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email


class PhoneForm(forms.ModelForm):
    code = forms.CharField(label='Code', widget=forms.TextInput(attrs={'style': "width: 100px;"
                                                                                "height: 34px;"
                                                                                "background-color: #fff;"
                                                                                "padding: 6px 12px;"
                                                                                "border: 1px solid #ccc;"
                                                                                "border-radius: 4px;"}))
    number = forms.CharField(label="Number",  widget=forms.TextInput(attrs={'style': "width: 300px;"
                                                                                     "height: 34px;"
                                                                                     "background-color: #fff;"
                                                                                     "padding: 6px 12px;"
                                                                                     "border: 1px solid #ccc;"
                                                                                     "border-radius: 4px;"}))

    class Meta:
        model = UserPhone
        fields = ('code', 'number')




