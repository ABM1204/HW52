from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        details = request.POST.get('details')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')

        if not description:
            return HttpResponseBadRequest('<h1>ERROR: Description is required</h1>')

        if status not in ['new', 'in_progress', 'done']:
            return HttpResponseBadRequest('<h1>ERROR: Invalid status</h1>')

        from datetime import datetime
        if due_date:
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                if due_date < datetime.today().date():
                    return HttpResponseBadRequest('<h1>ERROR: Due date cannot be in the past</h1>')
            except ValueError:
                return HttpResponseBadRequest('<h1>ERROR: Invalid date format</h1>')

        task = Task(description=description, details=details, status=status, due_date=due_date)
        task.save()
        return redirect('task_list')

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

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task_detail.html', {'task': task})

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.description = request.POST.get('description')
        task.details = request.POST.get('details')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')

        from datetime import datetime
        if task.due_date:
            try:
                task.due_date = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                if task.due_date < datetime.today().date():
                    return HttpResponseBadRequest('<h1>ERROR: Due date cannot be in the past</h1>')
            except ValueError:
                return HttpResponseBadRequest('<h1>ERROR: Invalid date format</h1>')

        task.save()
        return redirect('task_list')

    return render(request, 'edit_task.html', {'task': task})
