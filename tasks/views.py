from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Task
from .forms import TaskForm


# USER DASHBOARD
@login_required
def dashboard(request):

    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("dashboard")

    return render(request, "tasks/dashboard.html", {
        "tasks": tasks,
        "form": form
    })


# DELETE TASK
@login_required
def delete_task(request, id):

    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()

    return redirect("dashboard")


# EDIT TASK
@login_required
def edit_task(request, id):

    task = get_object_or_404(Task, id=id, user=request.user)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    return render(request, "tasks/edit_task.html", {
        "form": form
    })


# ADMIN LOGIN
def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")

        return render(request, "adminpanel/admin_login.html", {
            "error": "Invalid Admin Credentials"
        })

    return render(request, "adminpanel/admin_login.html")


# ADMIN DASHBOARD
@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    context = {
        "users": User.objects.count(),
        "tasks": Task.objects.count()
    }

    return render(request, "adminpanel/admin_dashboard.html", context)


# ADMIN USERS LIST
@login_required
def admin_users(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    users = User.objects.all()

    return render(request, "adminpanel/admin_users.html", {
        "users": users
    })


# ADMIN TASK LIST
@login_required
def admin_tasks(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    tasks = Task.objects.select_related("user").all()

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(user__username__icontains=search)
        )

    if status:
        tasks = tasks.filter(status=status)

    tasks = tasks.order_by("-created_at")

    return render(request, "adminpanel/admin_tasks.html", {
        "tasks": tasks
    })


# ADMIN EDIT TASK
@login_required
def admin_edit_task(request, id):

    if not request.user.is_staff:
        return redirect("dashboard")

    task = get_object_or_404(Task, id=id)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("admin_tasks")

    return render(request, "adminpanel/admin_edit_task.html", {
        "form": form
    })


# ADMIN DELETE TASK
@login_required
def admin_delete_task(request, id):

    if not request.user.is_staff:
        return redirect("dashboard")

    task = get_object_or_404(Task, id=id)
    task.delete()

    return redirect("admin_tasks")


# ADMIN VIEW USER TASKS
@login_required
def admin_user_tasks(request, id):

    if not request.user.is_staff:
        return redirect("dashboard")

    user = get_object_or_404(User, id=id)
    tasks = Task.objects.filter(user=user)

    return render(request, "adminpanel/admin_user_tasks.html", {
        "user": user,
        "tasks": tasks
    })

