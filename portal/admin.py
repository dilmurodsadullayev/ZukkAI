from django.contrib import admin
from .models import Topic, AITask, Submission, Analytics

admin.site.register(Topic)
admin.site.register(AITask)
admin.site.register(Submission)
admin.site.register(Analytics)