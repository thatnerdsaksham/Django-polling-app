"""Automated tests covering the main assignment requirements."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Choice, Question, Vote


class PollTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', password='pass12345!')
        self.q = Question.objects.create(question_text='Best language?')
        self.a = Choice.objects.create(question=self.q, choice_text='Python')
        self.b = Choice.objects.create(question=self.q, choice_text='C++')
        self.other_q = Question.objects.create(question_text='Other?')
        self.other_choice = Choice.objects.create(question=self.other_q, choice_text='X')

    def test_index_lists_only_active_polls(self):
        Question.objects.create(question_text='Hidden', is_active=False)
        resp = self.client.get(reverse('polls:index'))
        self.assertContains(resp, 'Best language?')
        self.assertNotContains(resp, 'Hidden')

    def test_voting_requires_login(self):
        resp = self.client.get(reverse('polls:detail', args=[self.q.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_valid_vote_is_recorded(self):
        self.client.login(username='tester', password='pass12345!')
        self.client.post(reverse('polls:detail', args=[self.q.id]), {'choice': self.a.id})
        self.a.refresh_from_db()
        self.assertEqual(self.a.votes, 1)
        self.assertEqual(Vote.objects.count(), 1)

    def test_no_choice_shows_error(self):
        self.client.login(username='tester', password='pass12345!')
        resp = self.client.post(reverse('polls:detail', args=[self.q.id]), {})
        self.assertContains(resp, 'Please select a choice before voting.')
        self.assertEqual(Vote.objects.count(), 0)

    def test_choice_from_other_poll_rejected(self):
        self.client.login(username='tester', password='pass12345!')
        self.client.post(reverse('polls:detail', args=[self.q.id]), {'choice': self.other_choice.id})
        self.assertEqual(Vote.objects.count(), 0)

    def test_cannot_vote_twice(self):
        self.client.login(username='tester', password='pass12345!')
        url = reverse('polls:detail', args=[self.q.id])
        self.client.post(url, {'choice': self.a.id})
        self.client.post(url, {'choice': self.b.id})
        self.assertEqual(Vote.objects.count(), 1)
        self.b.refresh_from_db()
        self.assertEqual(self.b.votes, 0)

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        c.login(username='tester', password='pass12345!')
        resp = c.post(reverse('polls:detail', args=[self.q.id]), {'choice': self.a.id})
        self.assertEqual(resp.status_code, 403)

    def test_results_page(self):
        resp = self.client.get(reverse('polls:results', args=[self.q.id]))
        self.assertEqual(resp.status_code, 200)

    def test_register_creates_user(self):
        self.client.post(reverse('register'), {
            'username': 'newuser', 'password1': 'Str0ng!Pass99', 'password2': 'Str0ng!Pass99'})
        self.assertTrue(User.objects.filter(username='newuser').exists())
