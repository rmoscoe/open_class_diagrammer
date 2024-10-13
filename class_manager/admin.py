from django.contrib import admin
from .models import *

class ModuleInline(admin.TabularInline):
    model = ProjectModule

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

class ModuleAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Class)
admin.site.register(Property)
admin.site.register(Method)
admin.site.register(Relationship)