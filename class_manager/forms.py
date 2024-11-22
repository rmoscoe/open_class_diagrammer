from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .helpers import prepare_dict_for_form
from .models import *

class MultipleInstanceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return getattr(obj, "name", obj.id)
    
class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    error_css_class = "invalid"

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
    error_css_class = "invalid"

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
    modules = MultipleInstanceField(queryset=Module.objects.none(), widget=forms.CheckboxSelectMultiple, required=False)
    error_css_class = "invalid"

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.request = request

        if self.user is not None:
            self.fields["modules"].queryset = Module.objects.filter(user=self.user)

        if request is not None and request.resolver_match.url_name == "project-update":
            instance = kwargs.get("instance")
            for field in self.fields.keys():
                self.fields[field].initial = instance[field]

    class Meta:
        model = Project
        fields = ["name", "description", "modules"]

class ModuleForm(ModelForm):
    projects = MultipleInstanceField(queryset=Module.objects.none(), widget=forms.CheckboxSelectMultiple)
    error_css_class = "invalid"

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.request = request

        if self.user is not None:
            self.fields["projects"].queryset = Project.objects.filter(user=self.user)

        if request is not None and request.resolver_match.url_name == "module-update":
            instance = kwargs.get("instance")
            for field in self.fields.keys():
                self.fields[field].initial = instance[field]

    class Meta:
        model = Module
        fields = ["name", "description", "projects", "color"]

class ClassForm(ModelForm):
    module = ModelChoiceField(queryset=Module.objects.none())
    error_css_class = "invalid"

    class Meta:
        model = Class
        fields = ["name", "module"]
    
    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.request = request
        if self.user:
            self.fields['module'].queryset = Module.objects.filter(user=self.user)
        if request and request.resolver_match.url_name == "class-update":
            instance = kwargs.get("instance")
            for field in self.fields.keys():
                self.fields[field].initial = instance[field] 

class PropertyForm(ModelForm):
    class_assoc = ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select, label="Class")
    data_type = forms.MultipleChoiceField(choices=prepare_dict_for_form(DATA_TYPE_CHOICES), widget=forms.CheckboxSelectMultiple)
    error_css_class = "invalid"

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        
        if self.user is not None:
            self.fields["class_assoc"].queryset = Class.objects.filter(user=self.user)
        if request and request.resolver_match.url_name == "property-update" and instance:
            if hasattr(instance, "data_type") and instance.data_type:
                existing_types = instance.data_type.split(" | ")
                valid_choices = [choice[0] for choice in self.fields['data_type'].choices]
                self.initial["data_type"] = [choice for choice in existing_types if choice in valid_choices]
            for field in self.fields.keys():
                if field != "data_type":
                    self.fields[field].initial = getattr(instance, field)
    
    def clean_data_type(self):
        selected_choices = self.cleaned_data["data_type"]
        return " | ".join(selected_choices)

    class Meta:
        model = Property
        fields = ["name", "class_assoc", "visibility", "data_type"]

class MethodForm(ModelForm):
    class_assoc = ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select, label="Class")
    error_css_class = "invalid"
    
    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        if self.user is not None:
            self.fields["class_assoc"].queryset = Class.objects.filter(user=self.user)
        if request and request.resolver_match.url_name == "method-update" and instance:
            for field in self.fields.keys():
                self.fields[field].initial = getattr(instance, field)
    
    class Meta:
        model = Method
        fields = ["name", "class_assoc", "visibility", "arguments", "return_type"]

class RelationshipForm(ModelForm):
    from_class = ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select)
    to_class = ModelChoiceField(queryset=Class.objects.none(), widget=forms.Select)
    error_css_class = "invalid"

    def __init__(self, *args, request=None, **kwargs):
        self.user = kwargs.pop("user", None)
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        class_queryset = None
        if self.user is not None:
            class_queryset = Class.objects.filter(user=self.user)
        else:
            print("User not given!")
            class_queryset = Class.objects.all()
        if request and request.resolver_match.url_name == "relationship-update" and instance:
            for field in self.fields.keys():
                self.fields[field].initial = getattr(instance, field)
        to_class_queryset = None
        if self.fields["from_class"].initial:
            f_class = None
            if self.user is not None:
                f_class = Class.objects.filter(user=self.user, name=self.fields["from_class"].initial).first()
            else:
                f_class = Class.objects.filter(name=self.fields["from_class"].initial).first()
            f_module = f_class.module
            to_class_queryset = Class.objects.filter(module=f_module)
        elif self.user is not None:
            to_class_queryset = Class.objects.filter(user=self.user)
        else:
            to_class_queryset = Class.objects.all()
        self.fields["to_class"].queryset = to_class_queryset
        from_class_queryset = None
        if self.fields["to_class"].initial:
            t_class = None
            if self.user is not None:
                t_class = Class.objects.filter(user=self.user, name=self.fields["to_class"].initial).first()
            else:
                t_class = Class.objects.filter(name=self.fields["to_class"].initial).first()
            t_module = t_class.module
            from_class_queryset = Class.objects.filter(module=t_module)
        elif self.user is not None:
            from_class_queryset = Class.objects.filter(user=self.user)
        else:
            from_class_queryset = Class.objects.all()
        self.fields["from_class"].queryset = from_class_queryset
    
    class Meta:
        model = Relationship
        fields = ["from_class", "to_class", "relationship_type"]