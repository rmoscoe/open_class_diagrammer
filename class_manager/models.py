from colorfield.fields import ColorField
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
    name = models.CharField(max_length=160, help_text="The name or title of the project.")
    description = models.TextField(null=True, blank=True, help_text="A description of the project (optional).")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ["name"]
    
    @classmethod
    def details(cls):
        return "A project is a complete application that includes at least one module."

class Module(Model):
    COLOR_PALETTE = [
        ("#000000", "Black",),
        ("#334155", "Slate",),
        ("#44403c", "Stone",),
        ("#854d0e", "Brown",),
        ("#dc2626", "Red",),
        ("#db2777", "Pink",),
        ("#e11d48", "Rose",),
        ("#ea580c", "Orange",),
        ("#d97706", "Amber",),
        ("#fcdb03", "Yellow",),
        ("#65a30d", "Lime",),
        ("#15803d", "Green",),
        ("#0d9488", "Teal",),
        ("#0284c7", "Sky",),
        ("#1d4ed8", "Blue",),
        ("#4338ca", "Indigo",),
        ("#6d28d9", "Violet",),
        ("#c026d3", "Fuchsia",),
        ("#ffffff", "White",)
    ]
    name = models.CharField(max_length=160, help_text="The name or title of the module.")
    description = models.TextField(null=True, blank=True, help_text="A description of the module (optional).")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    projects = models.ManyToManyField(Project, through="ProjectModule", help_text="A list of projects that include this module.")
    color = ColorField(format="hex", blank=True, default="#1d4ed8", help_text="The color of class diagrams in this module on UML diagrams.", samples=COLOR_PALETTE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ["name"]
    
    @classmethod
    def details(cls):
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
    name = models.CharField(max_length=160, help_text="The name of the class.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True, help_text="The module to which this class belongs.")
    relationships = models.ManyToManyField("self", through="Relationship", symmetrical=False, help_text="Related class(es).", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name_plural = "classes"
    
    @classmethod
    def details(cls):
        return "A class is a blueprint for objects in a software program. It is the core element of the Entity Relationship Diagram and is a member of a module. It includes properties and/or methods and can be related to other classes in various ways."

class BaseAttribute(Model):
    name = models.CharField(max_length=160)
    class_assoc = models.ForeignKey(Class, on_delete=models.CASCADE, help_text="The class that contains this attribute.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    visibility = models.CharField(max_length=80, choices=get_visibility_choices, help_text="Public (+): visible to any object that can view the class\n\nProtected (#): visible to objects that can view the class and are derived from the class\n\nPrivate (-): visibile only within the class and its instances", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True

class Property(BaseAttribute):
    data_type = models.CharField(max_length=255, null=True, blank=True, help_text="The data type (e.g., string, integer, Boolean, list, dictionary) of the property.")

    def get_data_type_display(self):
        selected_types = self.data_type.split(" | ")
        flattened_choices = flatten_dict(DATA_TYPE_CHOICES)
        return " | ".join(flattened_choices.get(choice, choice) for choice in selected_types)
    
    class Meta:
        verbose_name_plural = "properties"
    
    @classmethod
    def details(cls):
        return "A property is an attribute of a class and its instances."

class Method(BaseAttribute):
    arguments = models.CharField(max_length=255, null=True, blank=True, help_text="A list of the inputs to the method.")
    return_type = models.CharField(max_length=160, null=True, blank=True, help_text="The type of data output (returned) by the function.")
    
    @classmethod
    def details(cls):
        return "A method is an action (function) that a class or one of its instances can perform."

class Relationship(Model):
    from_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="from_class", help_text="The class in which the relationship originates.")
    to_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="to_class", help_text="The class to which the From Class is related.")
    relationship_type = models.CharField(max_length=80, choices=get_relationship_type_choices, help_text="The nature of the relationship between the classes (e.g., inheritance, composition, or cardinality, such as \"one-to-one\" or \"one-to-many\").")
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True)
    
    @classmethod
    def details(cls):
        return "A relationship describes the link between two classes, such as inheritance or ownership (e.g., one-to-many)"