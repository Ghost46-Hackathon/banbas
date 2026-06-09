# Banbas Project Notes

## What this project is

Banbas is a Django 5.2 application for a resort website plus an internal backoffice.

Public site features:
- Home page with featured rooms, amenities, gallery, and activities.
- Rooms, room details, amenities, gallery, activities, about, blog, and contact pages.
- CMS-like editing through Django admin for most public content.

Internal backoffice features:
- Reservation management.
- Inquiry management and conversion from inquiry to reservation.
- Analytics/dashboard.
- User management with role-based access.

The repository name and GitHub remote point to:
- `https://github.com/Ghost46-Hackathon/banbas.git`

## Tech stack

- Python 3.11+ expected.
- Django `5.2.6`
- SQLite database in development: `db.sqlite3`
- `django-ckeditor` for rich text content
- `whitenoise` for static file serving
- `gunicorn` for deployment via `Procfile`
- Bootstrap 5 and Font Awesome in templates

Dependencies are in `requirements.txt`.

## Main project layout

- `banbas_resort/`: Django project config
- `resort/`: public-facing app
- `backoffice/`: internal management app
- `templates/resort/`: public templates
- `templates/backoffice/`: internal templates
- `templates/emails/`: email templates
- `static/`: source static assets
- `staticfiles/`: collected and vendored static assets, including CKEditor
- `media/`: uploaded media, including videos
- `docs/`: project-specific implementation notes and bugfix writeups

## URL structure

Project URL config:
- `/admin/`: Django admin
- `/ckeditor/`: CKEditor upload routes
- `/`: public resort routes
- `/_internal/`: backoffice routes

Public routes in `resort/urls.py`:
- `/`
- `/rooms/`
- `/rooms/<pk>/`
- `/amenities/`
- `/activities/`
- `/activities/<pk>/`
- `/gallery/`
- `/blog/`
- `/blog/<slug>/`
- `/about/`
- `/contact/`

Backoffice routes in `backoffice/urls.py`:
- `/_internal/login/`
- `/_internal/logout/`
- `/_internal/`
- `/_internal/reservations/...`
- `/_internal/inquiries/...`
- `/_internal/analytics/`
- `/_internal/users/...`

## Important apps and models

### `resort` app

This is the public CMS/content layer.

Key models:
- `RoomType`: room metadata, public/private pricing toggle, features, image URL, availability.
- `RoomGallery`: images and videos attached to a room.
- `Amenity`: name, description, icon, image placeholder.
- `Activity`: rich content, availability, pricing, scheduling, featured flags.
- `GalleryCategory`: category model used to filter gallery items.
- `Gallery`: global gallery items with image/video support.
- `Contact`: inquiries submitted from the public contact form.
- `Blog`: rich text blog posts with slug, category, publish flag, excerpt generation.
- `AboutPage`: editable rich text content for the about page.
- `Resort`: single-instance site-wide resort info and hero media.
- `NavigationSettings`: controls visibility of nav items and booking CTA.

Behavior notes:
- `Resort` is effectively a singleton. Its `save()` method reuses the first record.
- `Blog` auto-generates `slug`, `excerpt`, and `published_date`.
- Public content pages mostly read the first `Resort` or `AboutPage` object rather than a multi-tenant setup.
- Several rich text fields are rendered with `|safe` in templates, so admin-authored content is trusted HTML.

### `backoffice` app

This is the internal operations layer.

Key models:
- `UserProfile`: one-to-one with Django `User`, stores role.
- `Reservation`: main reservation record with room counts, meal plan, currency, and audit metadata.
- `ReservationAuditLog`: change log for created/updated/deleted reservations, designed to preserve history even after deletion.

Role model:
- `viewer`: read-only access
- `agent`: can create/convert some operational records
- `admin`: full access including revenue and user management

Behavior notes:
- Reservation room quantities are stored in JSON under `room_types`.
- Reservation `number_of_rooms` can be derived from `room_types`.
- There is explicit logic for role checks in both decorators and mixins.
- User management routes are additionally wrapped with `admin_required(...)`.

## Views and behavior

Public site:
- `resort/views.py` is function-based.
- Home page pulls featured content and falls back to available rooms if fewer than 3 featured rooms exist.
- Gallery filtering uses `GalleryCategory.slug` first and falls back to the legacy `category` char field.
- Contact form creates a `Contact` record and tries to send notification email through `BanbasEmailService`.

Backoffice:
- `backoffice/views.py` uses a mix of class-based views and role mixins.
- Dashboard computes occupancy and, for admins, currency-converted revenue.
- Reservation list supports search and date filtering.
- Reservation detail exposes recent audit logs.
- Inquiry conversion turns public contact records into internal reservation workflow.

## Forms and validation

Notable forms:
- `resort/forms.py`: public contact form
- `backoffice/forms.py`: reservation form and backoffice user/profile form

Important validation behavior:
- Reservation form validates arrival/departure dates and room quantity consistency.
- User profile form now validates passwords with Django password validators before calling `set_password(...)`.
- New users without an explicit password get a random password.

## Settings and environment

Settings live in `banbas_resort/settings.py`.

Current configuration facts:
- `.env` is loaded with `python-dotenv`.
- `DEBUG` is environment-driven and defaults to `True`.
- In debug mode, default `ALLOWED_HOSTS` is `127.0.0.1, localhost`.
- In non-debug mode, `SECRET_KEY` and `ALLOWED_HOSTS` must be explicitly set.
- `CSRF_TRUSTED_ORIGINS` is environment-driven.
- Security flags are present for secure cookies, HSTS, referrer policy, nosniff, frame denial, and optional SSL redirect.
- Static source is `static/`.
- Static root is `staticfiles/`.
- Media root is `media/`.
- Database is SQLite.
- Email defaults to console backend unless overridden.

Important env vars from `.env.example`:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`

## Static assets and frontend notes

- `static/css/style.css` and related CSS files drive the public site.
- `static/js/main.js` contains custom front-end behavior for forms, date picking, and UX interactions.
- `staticfiles/ckeditor/` contains vendored third-party assets. This folder is noisy in static analysis results.
- `staticfiles/` also contains collected or bundled admin/static assets, not just hand-authored code.

Important caution:
- Security scanners report many findings in vendored CKEditor and legacy JS under `staticfiles/ckeditor/`. Those should generally be handled by upgrading/replacing vendored libraries, not by patching minified third-party files directly.

## Email behavior

Email handling uses `backoffice/email_service.py` and templates in `templates/emails/`.

Observed behavior:
- Public contact submissions attempt to notify staff.
- There are templates for new inquiry notification, welcome email, inquiry response, reservation confirmation, and reservation update.
- In development, email may only print to console unless SMTP env vars are configured.

## Management commands and scripts

Management commands:
- `python manage.py populate_sample_data`
- `python manage.py populate_about_page`
- `python manage.py create_test_users`
- `python manage.py test_email`
- `python manage.py update_currency_rates`
- `python manage.py view_deleted_reservations`

Operational scripts:
- `deploy.ps1`
- `auto-deploy-service.ps1`
- `webhook-listener.ps1`
- `run-network.ps1`
- `run-network.bat`
- `run_local_network.py`
- `run_with_ngrok.py`
- `populate_activities.py`
- `test-network.py`

There is a strong Windows/local-network deployment flavor in this repository.

## GitHub workflows

Defined workflows:
- `codeql.yml`: CodeQL analysis for JavaScript/TypeScript and Python.
- `deploy.yml`: local-server deployment notification workflow triggered on push to `main`.

The deploy workflow currently only notifies and archives a small deployment log artifact. It does not perform a real remote deployment by itself.

## Documentation in `docs/`

The `docs/` folder contains targeted notes for prior fixes and features:
- inquiry detail bugfix
- reservation edit bugfix
- currency conversion
- email functionality
- math template filters
- reservation deletion and audit behavior
- security implementation notes
- user edit error fix
- user management security

These docs are likely the best place to look before changing the matching subsystem.

## Current security state

Known recent improvements on the current branch:
- Stronger Django security defaults in settings.
- Password validation before setting backoffice user passwords.
- Safer GitHub Actions variable handling in `deploy.yml`.
- SRI integrity attributes added for Bootstrap and Font Awesome CDN assets.
- Some unsafe DOM write patterns in custom JS replaced with DOM-node construction.
- Dynamic regex use in `staticfiles/admin/js/inlines.js` replaced with string-based index replacement.

Still relevant:
- Vendored third-party JS under `staticfiles/ckeditor/` will keep generating security scanner noise until the dependency is upgraded or removed.
- Rich text content is trusted from admin authors and rendered as HTML on the public site.

## Local development notes

Standard flow:
- create virtualenv
- install `requirements.txt`
- run `python manage.py migrate`
- run `python manage.py populate_sample_data`
- run `python manage.py runserver`

Useful URLs:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/admin/`
- `http://127.0.0.1:8000/_internal/`

Environment note:
- This repo currently includes a `.venv` folder with Windows-style layout (`.venv/Scripts/python.exe`). On macOS/Linux that environment is not directly usable, so local checks may fail unless a native virtualenv is created.

## Things to watch before changing code

- Public templates and backoffice templates are both active; do not assume one is unused.
- `static/` and `staticfiles/` serve different purposes. Avoid editing vendored files unless the change is intentional.
- Some content models are effectively singleton-like and code assumes `first()` records exist.
- Reservations, inquiries, and user roles are tightly coupled in backoffice flows.
- Currency handling is admin-only in analytics and uses the custom `EXCHANGE_RATES` map.
- A lot of the project behavior depends on content created in admin rather than hardcoded fixtures.

## Current branch context

At the time this file was created, work was being done on:
- `codex/security-fix`

This branch already exists on GitHub and includes the recent security hardening work.
