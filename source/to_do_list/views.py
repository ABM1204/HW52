from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from .forms import TaskForm
from .models import Task

def task_list(request):
    if request.method == 'POST':
        task_ids = request.POST.getlist('tasks')
        if task_ids:
            Task.objects.filter(id__in=task_ids).delete()
            return redirect('task_list')
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponseNotFound('<h1>Task not found</h1>')
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete.html', {'task': task})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})
