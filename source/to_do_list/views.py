from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        description = request.POST.get('description')
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

        task = Task(description=description, status=status, due_date=due_date)
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
