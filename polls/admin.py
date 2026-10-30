"""Admin configuration: lets the admin manage polls without any custom UI."""
from django.contrib import admin

from .models import Choice, Question, Vote


class ChoiceInline(admin.TabularInline):
    """Edit a question's choices on the same page as the question."""
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'is_active', 'total_votes')
    list_filter = ('is_active', 'pub_date')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice', 'voted_at')
    list_filter = ('question',)
