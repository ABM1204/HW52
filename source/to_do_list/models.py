from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [('new', 'New'), ('in_progress', 'In process'), ('done', 'Done'),]

    description = models.CharField(max_length=200, verbose_name='Description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Status')
    due_date = models.DateField(null=True, blank=True, verbose_name='Done date')

    def __str__(self):
        return self.description
