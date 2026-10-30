"""Database models for the polling app (the "M" in MVT)."""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """A poll question created by the admin."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text="Untick to hide this poll from users.")

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.question_text

    def total_votes(self):
        """Sum of votes across all choices of this question."""
        return sum(choice.votes for choice in self.choices.all())


class Choice(models.Model):
    """One answer option belonging to a question."""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    """Records who voted on which question, so each user can vote only once per poll."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Database-level guard against duplicate votes
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} -> {self.choice}"
