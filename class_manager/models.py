from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model
from .helpers import flatten_dict
import uuid

# Create your models here.
DATA_TYPE_CHOICES = {
    "Any": "Any",
    "Primitives": {
        "Boolean": "Boolean",
        "Numeric": {
            "Number": "Number",
            "Integer": "Integer",
            "Double": "Double",
            "Float": "Float",
            "Complex": "Complex"
        },
        "Text": {
            "Character": "Character",
            "String": "String",
            "Binary": "Binary",
            "Bytes": "Bytes",
            "Bytearray": "Bytearray",
            "Memoryview": "Memoryview"
        }
    },
    "Collections": {
        "Ordered Collections": {
            "List/Linked List": "List/Linked List",
            "Array": "Array",
            "ArrayList": "ArrayList",
            "Tuple": "Tuple",
            "Set": "Set"
        },
        "Mappings": {
            "Dictionary": "Dictionary",
            "Map": "Map",
            "Struct": "Struct",
            "Object": "Object"
        }
    },
    "Null Values": {
        "Null": "Null",
        "None": "None",
        "Nil": "Nil",
        "Undefined": "Undefined"
    },
    "Other": "Other"
}

def get_relationship_type_choices():
    RELATIONSHIP_TYPE_CHOICES = ["inheritance", "composition", "one-to-one", "one-to-many", "many-to-many"]

    return {choice: choice for choice in RELATIONSHIP_TYPE_CHOICES}

def get_visibility_choices():
    VISIBILITY_CHOICES = ["public", "private", "protected"]
    
    return {choice: choice for choice in VISIBILITY_CHOICES}

class Project(Model):
    name = models.CharField(max_length=160)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ["name"]
    
    @property
    def details(self):
        return "A project is a complete application that includes at least one module."

class Module(Model):
    name = models.CharField(max_length=160)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    projects = models.ManyToManyField(Project, through="ProjectModule")
    color = models.CharField(max_length=7, blank=True, default="#1d4ed8")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ["name"]
    
    @property
    def details(self):
        return "A module is a functional component of a project and includes at least one class. A module could potentially be reused in (and thus, belong to) multiple projects. Examples include a blog, a learning system, a performance system, a succession management tool, and an individual development planning tool that are all part of a single talent management system (project)."

class ProjectModule(Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Check if project and module have the same user
        if self.project.user != self.module.user:
            raise ValidationError("Project and Module must belong to the same User.")
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["project", "module"], name="unique_project_module")
        ]

class Class(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)
    relationships = models.ManyToManyField("self", through="Relationship", symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name_plural = "classes"
    
    @property
    def details(self):
        return "A class is a blueprint for objects in a software program. It is the core element of the Entity Relationship Diagram and is a member of a module. It includes properties and/or methods and can be related to other classes in various ways."

class BaseAttribute(Model):
    name = models.CharField(max_length=160)
    class_assoc = models.ForeignKey(Class, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    visibility = models.CharField(max_length=80, choices=get_visibility_choices)

class Property(BaseAttribute):
    data_type = models.CharField(max_length=255, null=True, blank=True)

    def get_data_type_display(self):
        selected_types = self.data_type.split(" | ")
        flattened_choices = flatten_dict(DATA_TYPE_CHOICES)
        return " | ".join(flattened_choices.get(choice, choice) for choice in selected_types)
    
    class Meta:
        verbose_name_plural = "properties"
    
    @property
    def details(self):
        return "A property is an attribute of a class and its instances."

class Method(BaseAttribute):
    arguments = models.CharField(max_length=255, null=True, blank=True)
    return_type = models.CharField(max_length=160, null=True, blank=True)
    
    @property
    def details(self):
        return "A method is an action (function) that a class or one of its instances can perform."

class Relationship(Model):
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="from_class")
    to_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="to_class")
    relationship_type = models.CharField(max_length=80, choices=get_relationship_type_choices)
    
    @property
    def details(self):
        return "A relationship describes the link between two classes, such as inheritance or ownership (e.g., one-to-many)"