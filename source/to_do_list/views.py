from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')

        if description:
            task = Task(description=description, status=status, due_date=due_date)
            task.save()
            return redirect('task_list')
        else:
            return HttpResponseNotFound('<h1>ERROR: no description</h1>')

    return render(request, 'add_task.html')


def delete_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return HttpResponseNotFound('<h1>Task not found</h1>')

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'delete.html', {'task': task})
