from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .helpers import prepare_dict_for_form
from .models import *

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        print(f"Valid: {valid}")
        if not valid:
            errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
            for field, field_errors in self.errors.items():
                if field != '__all__':
                    continue
                for error in field_errors:
                    errors.append(error)
        return valid

class UpdateUserForm(ModelForm):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)

        self.fields["username"].initial = getattr(self.user, "username", None)
        self.fields["first_name"].initial = getattr(self.user, "first_name", None)
        self.fields["last_name"].initial = getattr(self.user, "last_name", None)
        self.fields["email"].initial = getattr(self.user, "email", None)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

class ProjectForm(ModelForm):
    modules = forms.ModelMultipleChoiceField(queryset=Module.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)
        self.request = request

        if self.user is not None:
            self.fields["modules"].queryset = Module.objects.filter(user=self.user)

        if request is not None and request.resolver_match.url_name == "project-update":
            instance = kwargs.get("instance")
            for field in self.fields.keys():
                self.field[field].initial = instance[field]

    class Meta:
        model = Project
        fields = ["name", "description", "modules"]

class ModuleForm(ModelForm):
    projects = forms.ModelMultipleChoiceField(queryset=Module.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)
        self.request = request

        if self.user is not None:
            self.fields["projects"].queryset = Project.objects.filter(user=self.user)

        if request is not None and request.resolver_match.url_name == "module-update":
            instance = kwargs.get("instance")
            for field in self.fields.keys():
                self.field[field].initial = instance[field]

    class Meta:
        model = Module
        fields = ["name", "description", "projects", "color"]

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ["name", "module", "relationships"]

class PropertyForm(ModelForm):
    class_assoc = forms.ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select, label="Class")
    data_type = forms.MultipleChoiceField(choices=prepare_dict_for_form(DATA_TYPE_CHOICES), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)
        
        if self.user is not None:
            self.fields["class_assoc"].queryset = Class.objects.filter(user=self.user)
    
    def clean_data_type(self):
        selected_choices = self.cleaned_data["data_type"]
        return " | ".join(selected_choices)

    class Meta:
        model = Property
        fields = ["name", "class_assoc", "visibility", "data_type"]

class MethodForm(ModelForm):
    class_assoc = forms.ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select, label="Class")
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("user", None)
        super().__init__(*args, **kwargs)

        if self.user is not None:
            self.fields["class_assoc"].queryset = Class.objects.filter(user=self.user)
    
    class Meta:
        model = Method
        fields = ["name", "class_assoc", "visibility", "arguments", "return_type"]

class RelationshipForm(ModelForm):
    class Meta:
        model = Relationship
        fields = ["from_model", "to_model", "relationship_type"]