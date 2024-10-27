from class_manager.views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ClassListView, ClassDetailView, ClassCreateView, ClassUpdateView, PropertyListView, PropertyDetailView, PropertyCreateView, PropertyUpdateView, MethodListView, MethodDetailView, MethodCreateView, MethodUpdateView, RelationshipListView, RelationshipDetailView, RelationshipCreateView, RelationshipUpdateView, DiagramView
from django.urls import path

models = ["project", "module", "class", "property", "method"]
actions = ["list", "detail", "create", "update"]
paths = []
views = [ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ClassListView, ClassDetailView, ClassCreateView, ClassUpdateView, PropertyListView, PropertyDetailView, PropertyCreateView, PropertyUpdateView, MethodListView, MethodDetailView, MethodCreateView, MethodUpdateView, RelationshipListView, RelationshipDetailView, RelationshipCreateView, RelationshipUpdateView]
names = []

app_name = "class_manager"

urlpatterns = []

for m in models:
    for a in actions:
        p = [m, "<pk>", a] if a in ["detail", "update"] else [m, a]
        p = "/".join(p) + "/"
        n = "-".join([m, a])
        paths.append(p)
        names.append(n)

for i, p in enumerate(paths):
    urlpatterns.append(path(p, views[i].as_view(), name=names[i]))

urlpatterns += [path("project/<pk>/diagram/", DiagramView.as_view(), name="diagram")]