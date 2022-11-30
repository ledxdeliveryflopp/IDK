from django.contrib import admin
from .models import CustomUser, Choice, Question


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]
    readonly_fields = ['votes', 'voted_by', 'pub_date', 'life_time']


admin.site.register(Question, QuestionAdmin)
admin.site.register(CustomUser)
admin.site.register(Choice)
