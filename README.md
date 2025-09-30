# Banbas Resort

A modern Django website for Banbas Resort with rooms, amenities, gallery, and contact features. Includes sample data and a responsive UI built with Bootstrap.

## Prerequisites
- Git
- Python 3.11+

## Quick Start

Follow the steps for your OS to set up and run the project locally.

### Windows (PowerShell)
```powershell
# 1) Clone the repo
git clone https://github.com/Ghost46-Hackathon/banbas.git
cd banbas

# 2) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Apply migrations and load sample data
python manage.py migrate
python manage.py populate_sample_data

# 5) Run the development server
python manage.py runserver
```

### macOS and Linux (bash/zsh)
```bash
# 1) Clone the repo
git clone https://github.com/Ghost46-Hackathon/banbas.git
cd banbas

# 2) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Apply migrations and load sample data
python manage.py migrate
python manage.py populate_sample_data

# 5) Run the development server
python manage.py runserver
```

## Accessing the App
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
  - Default superuser: created via `python manage.py createsuperuser` (or use the one you created)

## Common Commands
```bash
# Make database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for the admin panel
python manage.py createsuperuser

# Populate sample content (rooms, amenities, gallery, resort info)
python manage.py populate_sample_data

# Collect static files (for production setups)
python manage.py collectstatic
```

## Notes
- Development server is for local use only. For production, configure `ALLOWED_HOSTS`, set `DEBUG = False`, and use a proper WSGI/ASGI server.
- Dependencies are pinned in `requirements.txt`.
