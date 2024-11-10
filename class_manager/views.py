from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .forms import RegistrationForm, UpdateUserForm, ProjectForm, ModuleForm, ClassForm, PropertyForm, MethodForm, RelationshipForm # , UserForm
from .helpers import build_color_theme
from .models import *

# Create your views here.
DEFAULT_COLORS = {
    "black": {
        "display_name": "Black",
        "primary_color": "#000000",
        "content_color": "neutral-500",
        "border_color": "neutral-200",
        "dark_primary_color": "#000000",
        "dark_content_color": "neutral-600",
        "dark_border_color": "neutral-300"
    },
    "slate-700": {
        "display_name": "Slate",
        "primary_color": "#334155",
        "content_color": "slate-400",
        "border_color": "slate-200",
        "dark_primary_color": "#94a3b8",
        "dark_content_color": "slate-500",
        "dark_border_color": "slate-300"
    },
    "stone-700": {
        "display_name": "Stone",
        "primary_color": "#44403c",
        "content_color": "stone-400",
        "border_color": "stone-200",
        "dark_primary_color": "#a8a29e",
        "dark_content_color": "stone-500",
        "dark_border_color": "stone-300"
    },
    "yellow-800": {
        "display_name": "Brown",
        "primary_color": "#854d0e",
        "content_color": "yellow-600",
        "border_color": "cream",
        "dark_primary_color": "#713f12",
        "dark_content_color": "yellow-700",
        "dark_border_color": "oatmeal"
    },
    "red-600": {
        "display_name": "Red",
        "primary_color": "#dc2626",
        "content_color": "red-300",
        "border_color": "red-100",
        "dark_primary_color": "#ef4444",
        "dark_content_color": "red-400",
        "dark_border_color": "red-200"
    },
    "pink-600": {
        "display_name": "Pink",
        "primary_color": "#db2777",
        "content_color": "pink-300",
        "border_color": "pink-100",
        "dark_primary_color": "#ec4899",
        "dark_content_color": "pink-400",
        "dark_border_color": "pink-200"
    },
    "rose-600": {
        "display_name": "Rose",
        "primary_color": "#e11d48",
        "content_color": "rose-300",
        "border_color": "rose-100",
        "dark_primary_color": "#f43f5e",
        "dark_content_color": "rose-400",
        "dark_border_color": "rose-200"
    },
    "orange-600": {
        "display_name": "Orange",
        "primary_color": "#ea580c",
        "content_color": "orange-300",
        "border_color": "orange-100",
        "dark_primary_color": "#f97316",
        "dark_content_color": "orange-400",
        "dark_border_color": "orange-200"
    },
    "amber-600": {
        "display_name": "Amber",
        "primary_color": "#d97706",
        "content_color": "amber-300",
        "border_color": "amber-100",
        "dark_primary_color": "#f59e0b",
        "dark_content_color": "amber-400",
        "dark_border_color": "amber-200"
    },
    "bright-yellow": {
        "display_name": "Yellow",
        "primary_color": "#fcdb03",
        "content_color": "yellow-200",
        "border_color": "yellow-100",
        "dark_primary_color": "#ffe01a",
        "dark_content_color": "yellow-300",
        "dark_border_color": "yellow-200"
    },
    "lime-600": {
        "display_name": "Lime",
        "primary_color": "#65a30d",
        "content_color": "lime-300",
        "border_color": "lime-100",
        "dark_primary_color": "#84cc16",
        "dark_content_color": "lime-400",
        "dark_border_color": "lime-200"
    },
    "green-700": {
        "display_name": "Green",
        "primary_color": "#15803d",
        "content_color": "green-300",
        "border_color": "green-100",
        "dark_primary_color": "#16a34a",
        "dark_content_color": "green-400",
        "dark_border_color": "green-200"
    },
    "teal-600": {
        "display_name": "Teal",
        "primary_color": "#0d9488",
        "content_color": "teal-200",
        "border_color": "teal-100",
        "dark_primary_color": "#14b8a6",
        "dark_content_color": "teal-300",
        "dark_border_color": "teal-200"
    },
    "sky-600": {
        "display_name": "Sky",
        "primary_color": "#0284c7",
        "content_color": "sky-300",
        "border_color": "sky-100",
        "dark_primary_color": "#0ea5e9",
        "dark_content_color": "sky-400",
        "dark_border_color": "sky-200"
    },
    "blue-700": {
        "display_name": "Blue",
        "primary_color": "#1d4ed8",
        "content_color": "blue-300",
        "border_color": "blue-100",
        "dark_primary_color": "#2563eb",
        "dark_content_color": "blue-400",
        "dark_border_color": "blue-200"
    },
    "indigo-700": {
        "display_name": "Indigo",
        "primary_color": "#4338ca",
        "content_color": "indigo-300",
        "border_color": "indigo-100",
        "dark_primary_color": "#4f46e5",
        "dark_content_color": "indigo-400",
        "dark_border_color": "indigo-200"
    },
    "violet-700": {
        "display_name": "Violet",
        "primary_color": "#6d28d9",
        "content_color": "violet-300",
        "border_color": "violet-100",
        "dark_primary_color": "#7c3aed",
        "dark_content_color": "violet-400",
        "dark_border_color": "violet-200"
    },
    "fuchsia-600": {
        "display_name": "Fuchsia",
        "primary_color": "#c026d3",
        "content_color": "fuchsia-300",
        "border_color": "fuchsia-100",
        "dark_primary_color": "#d946ef",
        "dark_content_color": "fuchsia-400",
        "dark_border_color": "fuchsia-200"
    },
    "white": {
        "display_name": "White",
        "primary_color": "#ffffff",
        "content_color": "zinc-50",
        "border_color": "zinc-400",
        "dark_primary_color": "#ffffff",
        "dark_content_color": "zinc-100",
        "dark_border_color": "zinc-300"
    }
}


#================================#
#             MIXINS             #
#================================#

class AnonymousUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy("workbench"))

class OCDListMixin:
    template_name = "class_manager/list.html"

    # def get_queryset(self):
    #     return Project.objects.filter(user=self.request.user.id)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["create_route"] = "class_manager:" + self.model.__name__.lower() + "-create"
        context["detail_route"] = "class_manager" + self.model.__name__.lower() + "-detail"
        return context

class OCDDetailMixin:
    template_name = "class_manager/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["create_route"] = "class_manager:" + self.model.__name__.lower() + "-create"
    
class OCDEditMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

class OCDDeleteMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["delete_route"] = self.request.path
        return context

    def delete(self, request, *args, **kwargs):
        model = self.model
        try:
            if 'pk' in kwargs:
                obj = get_object_or_404(model, id=kwargs["pk"])
            else:
                id = request.GET.get("id")
                if id is None:
                    raise Http404
                obj = get_object_or_404(model, id=int(id))
            if hasattr(obj, "user") and self.request.user != obj.user:
                raise Http404
            obj.delete()
            if 'detail' in request.resolver_match.url_name:
                return HttpResponse("OK", status=200)
            return self.get(self.request)
        except Exception as e:
            print(e)
            return HttpResponse(e, status=500)
        

#================================#
#     PAGE AND USER VIEWS        #
#================================#

class HomePageView(TemplateView):
    template_name = "class_manager/home.html"

class SignupView(CreateView):
    model = User
    template_name = "class_manager/signup.html"
    success_url = reverse_lazy("login")
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        if form:
            context["form_errors"] = form.errors
        return context
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class OpenClassDiagrammerLoginView(AnonymousUserMixin, LoginView):
    model = User
    template_name = "class_manager/login.html"
    success_url = reverse_lazy("workbench")
    form_class = AuthenticationForm

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "class_manager/account_update.html"
    form_class = UpdateUserForm

    def get_success_url(self):
        return reverse("account-detail", kwargs={"pk": self.request.user.id})
    
class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "class_manager/user_detail.html"

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)
    
class WorkbenchView(LoginRequiredMixin, TemplateView):
    template_name = "class_manager/workbench.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.filter(user=self.request.user.id)
        modules = Module.objects.filter(user=self.request.user.id)
        classes = Class.objects.filter(user=self.request.user.id)
        properties = Property.objects.filter(user=self.request.user.id)
        methods = Method.objects.filter(user=self.request.user.id)
        relationships = Relationship.objects.filter(from_model__in=classes)
        context["data"] = {
            "projects": {
                "icon_class": "fa-solid fa-list-check",
                "list": "class_manager:project-list",
                "add": "class_manager:project-create",
                "details": Project.details,
                "objects": projects
            },
            "modules": {
                "icon_class": "fa-solid fa-robot",
                "list": "class_manager:module-list",
                "add": "class_manager:module-create",
                "details": Module.details,
                "objects": modules
            },
            "classes": {
                "icon_class": "fa-solid fa-shapes",
                "list": "class_manager:class-list",
                "add": "class_manager:class-create",
                "details": Class.details,
                "objects": classes
            },
            "properties": {
                "icon_class": "fa-solid fa-arrows-to-dot",
                "list": "class_manager:property-list",
                "add": "class_manager:property-create",
                "details": Property.details,
                "objects": properties
            },
            "methods": {
                "icon_class": "fa-solid fa-rocket",
                "list": "class_manager:method-list",
                "add": "class_manager:method-create",
                "details": Method.details,
                "objects": methods
            },
            "relationships": {
                "icon_class": "fa-solid fa-sitemap",
                "list": "class_manager:relationship-list",
                "add": "class_manager:relationship-create",
                "details": Relationship.details,
                "objects": relationships
            }
        }
        return context


#================================#
#         PROJECT VIEWS          #
#================================#

class ProjectListView(LoginRequiredMixin, OCDListMixin, OCDDeleteMixin, ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user.id)

class ProjectDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Project

class ProjectCreateView(LoginRequiredMixin, OCDEditMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "class_manager/create.html"

class ProjectUpdateView(LoginRequiredMixin, OCDEditMixin, OCDDeleteMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "class_manager/update.html"


#================================#
#         MODULE VIEWS           #
#================================#
    
class ModuleListView(LoginRequiredMixin, OCDListMixin, OCDDeleteMixin, ListView):
    model = Module

    def get_queryset(self):
        return Module.objects.prefetch_related("projects").filter(user=self.request.user.id)

class ModuleDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Module

    def get_queryset(self):
        return Module.objects.prefetch_related("projects").filter(user=self.request.user.id)

class ModuleCreateView(LoginRequiredMixin, OCDEditMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "class_manager/create.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["color_choices"] = DEFAULT_COLORS
        return context

class ModuleUpdateView(LoginRequiredMixin, OCDEditMixin, OCDDeleteMixin, UpdateView):
    model = Module
    form_class = ProjectForm
    template_name = "class_manager/update.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["color_choices"] = DEFAULT_COLORS
        return context


#================================#
#          CLASS VIEWS           #
#================================#

class ClassListView(LoginRequiredMixin, OCDListMixin, OCDDeleteMixin, ListView):
    model = Class

    def get_queryset(self):
        return Class.objects.select_related("module").prefetch_related("module__projects").filter(user=self.request.user.id)
    
class ClassDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Class

    def get_queryset(self):
        return Class.objects.select_related("module").prefetch_related("module__projects").filter(user=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relationship_form = RelationshipForm(initial={"from_model": self.object})
        context["relationship_form"] = relationship_form
        return context
    
    def get_success_url(self):
        return reverse("class-detail", kwargs={"pk": self.object.id})

class ClassCreateView(LoginRequiredMixin, OCDEditMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = "class_manager/create.html"

class ClassUpdateView(LoginRequiredMixin, OCDEditMixin, OCDDeleteMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "class_manager/update.html"


#================================#
#         PROPERTY VIEWS         #
#================================#

class PropertyListView(LoginRequiredMixin, OCDListMixin, OCDDeleteMixin, ListView):
    model = Property

    def get_queryset(self):
        return Property.objects.select_related("class_assoc").select_related("class_assoc__module").prefetch_related("class_assoc__module__projects").filter(user=self.request.user.id)

class PropertyDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Property

    def get_queryset(self):
        return Property.objects.select_related("class_assoc").select_related("class_assoc__module").prefetch_related("class_assoc__module__projects").filter(user=self.request.user.id)

class PropertyCreateView(LoginRequiredMixin, OCDEditMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = "class_manager/create.html"

class PropertyUpdateView(LoginRequiredMixin, OCDEditMixin, OCDDeleteMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = "class_manager/update.html"


#================================#
#          METHOD VIEWS          #
#================================#

class MethodListView(LoginRequiredMixin, OCDListMixin, OCDDeleteMixin, ListView):
    model = Method

    def get_queryset(self):
        return Method.objects.select_related("class_assoc").select_related("class_assoc__module").prefetch_related("class_assoc__module__projects").filter(user=self.request.user.id)

class MethodDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Method

    def get_queryset(self):
        return Method.objects.select_related("class_assoc").select_related("class_assoc__module").prefetch_related("class_assoc__module__projects").filter(user=self.request.user.id)

class MethodCreateView(LoginRequiredMixin, OCDEditMixin, CreateView):
    model = Method
    form_class = MethodForm
    template_name = "class_manager/create.html"

class MethodUpdateView(LoginRequiredMixin, OCDEditMixin, OCDDeleteMixin, UpdateView):
    model = Method
    form_class = MethodForm
    template_name = "class_manager/update.html"


#================================#
#       RELATIONSHIP VIEWS       #
#================================#

class RelationshipListView(LoginRequiredMixin, OCDDeleteMixin, ListView):
    model = Relationship
    template_name = "class_manager/list.html"

    def get_queryset(self):
        return Relationship.objects.select_related("from_class", "to_class").prefetch_related("from_class__module", "to_class__module").filter(user=self.request.user.id)

class RelationshipDetailView(LoginRequiredMixin, OCDDetailMixin, OCDDeleteMixin, DetailView):
    model = Relationship

    def get_queryset(self):
        return Relationship.objects.select_related("from_class", "to_class").prefetch_related("from_class__module", "to_class__module").filter(user=self.request.user.id)

class RelationshipCreateView(LoginRequiredMixin, CreateView):
    model = Relationship
    form_class = RelationshipForm
    template_name = "class_manager/create.html"

    def get_success_url(self):
        if self.request.POST.get("page", "relationship-detail") == "class-detail":
            return reverse("class-detail", kwargs={"pk": self.object.from_model.id})
        else:
            return reverse("relationship-detail", kwargs={"pk", self.object.id})

class RelationshipUpdateView(LoginRequiredMixin, OCDDeleteMixin, UpdateView):
    model = Relationship
    form_class = RelationshipForm
    template_name = "class_manager/update.html"

    def get_success_url(self):
        if self.request.POST.get("page", "relationship-detail") == "class-detail":
            return reverse("class-detail", kwargs={"pk": self.object.from_model.id})
        else:
            return reverse("relationship-detail", kwargs={"pk", self.object.id})
        

#================================#
#          DIAGRAM VIEW          #
#================================#

class DiagramView(LoginRequiredMixin, TemplateView):
    template_name = "class_manager/diagram.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = Project.objects.prefetch_related(
            "module_set",
            "module_set__class_set",
            "module_set__class_set__property_set",
            "module_set__class_set__method_set",
            "module_set__class_set__relationships"
        ).get(id=self.kwargs["pk"])
        context["project"] = project
        colors = DEFAULT_COLORS.copy()
        default_primary_colors = [color["primary_color"] for color in DEFAULT_COLORS]
        counter = 1
        for module in project.module_set:
            if module.color not in default_primary_colors:
                color = build_color_theme(module.color)
                colors[f"custom_color_{counter}"] = color
                counter += 1
        context["colors"] = colors
        return context