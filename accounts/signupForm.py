from django import forms
from django_countries.fields import CountryField
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import CustomUser
from datetime import date


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        help_text="Please Enter Your Username.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="Username",
        error_messages={"Required": "Enter Your Username"},
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Please Enter Your FirstName.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="First Name",
        error_messages={"error": "Enter Your First Name"},
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Please Enter Your LastName.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="Last Name",
        error_messages={"error": "Enter Your Last Name"},
    )
    picture = forms.ImageField(
        required=False,
        help_text="Add Your Profile Picture.",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        error_messages={"error": "Add Your Profile Picture."},
        label="Image",
    )
    address1 = forms.CharField(
        max_length=255,
        required=False,
        help_text="Please Enter Your First Location.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="First Location",
        error_messages={"error": "Enter Your First Location"},
    )
    address2 = forms.CharField(
        max_length=255,
        required=False,
        help_text="Please Enter Your Second Location.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="Second Location",
        error_messages={"error": "Enter Your Second Location."},
    )
    country = CountryField().formfield(
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Country",
        required=True,
        error_messages={"required": "Enter Your Country"},
    )

    city = forms.CharField(
        max_length=100,
        required=True,
        help_text="Please Enter City.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="City",
        error_messages={"error": "Enter Your City"},
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        help_text="Please Enter Your Email.",
        widget=forms.TextInput(attrs={"type": "email", "class": "form-control"}),
        label="Email",
        error_messages={"error": "Enter Your Email"},
    )
    phone_number = forms.CharField(
        max_length=50,
        required=True,
        help_text="Please Enter Phone Number.",
        widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
        label="Phone number",
        error_messages={"error": "Enter Your Phone number"},
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        help_text="Please Enter Your Password.",
        widget=forms.TextInput(attrs={"type": "password", "class": "form-control"}),
        label="Password",
        error_messages={"required": "Enter Your Password"},
    )
    password2 = forms.CharField(
        max_length=100,
        required=True,
        help_text="Please Enter Your Confirm Password.",
        widget=forms.TextInput(attrs={"type": "password", "class": "form-control"}),
        label="Confirm Password",
        error_messages={"required": "Enter Your Confirm Password"},
    )
    birth_date = forms.DateField(
        required=False,
        label="Birth Date",
        help_text="Your Age must 18 or grather.",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        error_messages={"required": "Please Enter Your Birth Date"},
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    # Write the limit of birth date
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        today = date.today()
        age = (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )
        if age < 18 or age > 100:
            raise forms.ValidationError("Your age must be between 18 and 100.")
        return birth_date

    # write the limit of username
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This Username Already Taken.")
        return username

    # write the limit of email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This Eamil Already Taken.")
        return email

    # write the limit password
    def clean_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if not password2:
            password2 = self.data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        elif len(password1) < 8:
            raise forms.ValidationError(
                "Your password must be 8 or greater than 8 characters."
            )
        return password1
