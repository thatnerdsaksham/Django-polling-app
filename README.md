# Django Polling / Voting Application

Users view poll questions, vote on choices and see results; an admin manages polls through Django admin.

## Quick start (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py runserver
```

Open http://127.0.0.1:8000/

The project ships with `db.sqlite3` already containing sample data, so it works immediately.

### Demo accounts

| Role | Username | Password |
|---|---|---|
| Admin (`/admin/`) | `admin` | `Admin@12345` |
| Voter | `demo1`, `demo2`, `demo3` | `Demo@12345` |

`demo1` to `demo3` have already voted on the first poll (so you can see results and the "already voted" message). Register a new user, or use another poll, to try voting.

### Starting from an empty database instead

```powershell
del db.sqlite3
python manage.py migrate
python manage.py loaddata sample_data.json
python manage.py createsuperuser
python manage.py runserver
```

### Run the automated tests

```powershell
python manage.py test
```

## Project layout

```
manage.py
pollsite/            project config: settings.py, urls.py
polls/
    models.py        Question, Choice, Vote
    admin.py         admin registration (inline choices)
    forms.py         VoteForm (validation)
    views.py         index, detail (vote), results, register
    urls.py          app routes
    tests.py         9 automated tests
    templates/
        polls/       base, index, detail, results
        registration/ login, register
sample_data.json     sample questions and choices
```

## How MVT, URLs and admin are used

**Model (M).** `polls/models.py` defines three tables. `Question` holds the text, publish date and an `is_active` flag. `Choice` belongs to a question through a `ForeignKey` and stores its vote count. `Vote` links a user, a question and the chosen choice, with `unique_together = ('user', 'question')` so a user can vote only once per poll. `makemigrations` turns these classes into a migration file, and `migrate` creates the tables.

**View (V).** `polls/views.py` holds the logic:
- `index` lists active polls.
- `detail` (login required) shows the form on GET. On POST it validates the form, saves a `Vote` and increments the choice counter inside one database transaction.
- `results` calculates counts and percentages.
- `register` creates new users with Django's `UserCreationForm`.

**Template (T).** `base.html` is the shared layout (navigation, messages). `index.html`, `detail.html` and `results.html` extend it and render the data the views pass in. `login.html` and `register.html` live in `registration/` so Django's auth views find them.

**URL routing.** `pollsite/urls.py` is the main router: `admin/`, `accounts/` (built-in login and logout), `accounts/register/`, and everything else delegated to `polls/urls.py` via `include()`. `polls/urls.py` uses `app_name = 'polls'` and named routes (`''`, `<int:question_id>/`, `<int:question_id>/results/`), so templates link with `{% url 'polls:detail' question.id %}`.

**Request flow.** Browser → `pollsite/urls.py` → `polls/urls.py` → view → model/ORM (database) → template → HTML response.

**Admin.** `polls/admin.py` registers `Question` with a `ChoiceInline`, so an admin creates a question and its choices on one page. List display, filters and search let the admin find polls quickly, and unticking `is_active` hides a poll from users. `Vote` is registered so the admin can audit who voted.

**Form validation.** `VoteForm` is a `ModelChoiceField` limited to the current question's choices. Submitting nothing shows "Please select a choice before voting." and a choice id from another poll is rejected.

**Security.**
- `{% csrf_token %}` in every POST form (tested: a POST without the token returns 403).
- `@login_required` on voting.
- Duplicate votes blocked twice: by a check in the view and by the database constraint.
- The vote count uses an `F()` expression, so simultaneous votes cannot overwrite each other.
- The logout button is a POST form, as current Django requires.

## Requirements coverage

| # | Requirement | Where |
|---|---|---|
| 1 | Models and migrations | `polls/models.py`, `polls/migrations/0001_initial.py` |
| 2 | Clean URL routing and view logic | `pollsite/urls.py`, `polls/urls.py`, `polls/views.py` |
| 3 | Form validation and error handling | `polls/forms.py`, error display in `detail.html`, duplicate-vote handling |
| 4 | Django admin for data management | `polls/admin.py` |
| 5 | CSRF and authentication | `{% csrf_token %}`, `@login_required`, login/register/logout |
| 6 | Clean, commented code | Docstrings and comments throughout |
| 7 | Working demo with sample data | `db.sqlite3`, `sample_data.json`, demo accounts above |
