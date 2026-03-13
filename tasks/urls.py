from django.urls import path
from . import views

urlpatterns = [

path('dashboard/',views.dashboard,name='dashboard'),
path('delete/<int:id>/',views.delete_task,name='delete'),
path('edit-task/<int:id>/',views.edit_task,name='edit_task'),

path("admin-login/",views.admin_login,name="admin_login"),
path("admin-dashboard/",views.admin_dashboard,name="admin_dashboard"),
path("admin-users/",views.admin_users,name="admin_users"),
path("admin-tasks/",views.admin_tasks,name="admin_tasks"),
path("admin-edit-task/<int:id>/",views.admin_edit_task,name="admin_edit_task"),
path("admin-delete-task/<int:id>/",views.admin_delete_task,name="admin_delete_task"),
path("admin-user-tasks/<int:id>/",views.admin_user_tasks,name="admin_user_tasks"),

]