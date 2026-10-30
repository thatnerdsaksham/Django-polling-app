"""View logic (the "V" in MVT): fetch data, validate forms, render templates."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VoteForm
from .models import Choice, Question, Vote


def index(request):
    """List all active polls, newest first."""
    questions = Question.objects.filter(is_active=True)
    return render(request, 'polls/index.html', {'questions': questions})


@login_required  # only logged-in users may vote
def detail(request, question_id):
    """Show the voting form (GET) and record a valid vote (POST)."""
    question = get_object_or_404(Question, pk=question_id, is_active=True)

    # One vote per user per poll
    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.info(request, "You have already voted on this poll.")
        return redirect('polls:results', question_id=question.id)

    # Bind the form only on POST (an empty POST dict is falsy, so `or None` would hide errors)
    form = VoteForm(question, request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        choice = form.cleaned_data['choice']
        try:
            # atomic: either both the Vote row and the counter update, or neither
            with transaction.atomic():
                Vote.objects.create(user=request.user, question=question, choice=choice)
                Choice.objects.filter(pk=choice.pk).update(votes=F('votes') + 1)
        except IntegrityError:
            messages.error(request, "Duplicate vote blocked.")
        else:
            messages.success(request, "Your vote was recorded!")
        return redirect('polls:results', question_id=question.id)

    return render(request, 'polls/detail.html', {'question': question, 'form': form})


def results(request, question_id):
    """Show vote counts and percentages for a poll."""
    question = get_object_or_404(Question, pk=question_id)
    total = question.total_votes()
    rows = [
        {
            'text': c.choice_text,
            'votes': c.votes,
            'percent': round(c.votes * 100 / total) if total else 0,
        }
        for c in question.choices.all()
    ]
    return render(request, 'polls/results.html', {'question': question, 'rows': rows, 'total': total})


def register(request):
    """Sign-up page using Django's built-in user creation form."""
    form = UserCreationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Account created. Please log in.")
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})
