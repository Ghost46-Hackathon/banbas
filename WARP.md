# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**banbas** is a Django-based resort website featuring a modern, responsive design for Banbas Resort. The project includes a complete resort management system with rooms, amenities, gallery, and contact functionality.

### Repository Information
- **GitHub Repository**: https://github.com/Ghost46-Hackathon/banbas.git
- **Main Branch**: main
- **Project Type**: Django Web Application
- **Python Version**: 3.11+
- **Framework**: Django 5.2.6

## Architecture

This Django project follows the standard Django architecture pattern:

### Project Structure
- **`banbas_resort/`** - Main Django project configuration
  - `settings.py` - Django settings with custom configurations for static/media files
  - `urls.py` - Main URL routing including resort app and admin
  - `wsgi.py` - WSGI configuration for deployment

- **`resort/`** - Main Django app containing all resort functionality
  - `models.py` - Data models (Resort, RoomType, Amenity, Gallery, Contact)
  - `views.py` - View logic for all pages (home, rooms, amenities, gallery, contact, about)
  - `admin.py` - Django admin configuration
  - `forms.py` - Django forms for contact functionality
  - `urls.py` - App-specific URL routing

- **`templates/resort/`** - HTML templates with Bootstrap 5 styling
  - `base.html` - Base template with navigation and footer
  - `home.html` - Landing page with hero section and featured content
  - `contact.html` - Contact form page
  - Additional templates for rooms, amenities, gallery, etc.

- **`static/`** - Static files (CSS, JavaScript, images)
  - `css/style.css` - Custom CSS with modern styling and animations
  - `js/main.js` - JavaScript for interactive features

### Database Models
- **Resort**: Single instance model for resort information
- **RoomType**: Different types of rooms with pricing and amenities
- **Amenity**: Resort facilities and services
- **Gallery**: Photo gallery with categories
- **Contact**: Contact form submissions

## Common Commands

### Django Development
```bash
# Start the development server
python manage.py runserver

# Create and apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Populate sample data (custom command)
python manage.py populate_sample_data

# Collect static files for production
python manage.py collectstatic

# Django shell for debugging/testing
python manage.py shell
```

### Database Management
```bash
# Reset database (removes all data)
# Delete db.sqlite3 file then run:
python manage.py migrate
python manage.py populate_sample_data

# Check database structure
python manage.py dbshell
```

### Git Operations
```bash
# Check repository status
git status

# View commit history
git log --oneline

# Pull latest changes
git pull origin main

# Push changes
git push origin main
```

## Development Notes

### Admin Access
- **URL**: http://localhost:8000/admin/
- **Default credentials**: admin / admin (created during setup)
- **Features**: Manage resort info, rooms, amenities, gallery, and contact messages

### Key URLs
- **Home**: http://localhost:8000/
- **Rooms**: http://localhost:8000/rooms/
- **Amenities**: http://localhost:8000/amenities/
- **Gallery**: http://localhost:8000/gallery/
- **About**: http://localhost:8000/about/
- **Contact**: http://localhost:8000/contact/
- **Admin**: http://localhost:8000/admin/

### Sample Data
The project includes a management command to populate sample data:
- 5 different room types with realistic pricing
- 8 amenities (6 featured)
- 8 gallery images across different categories
- Sample contact messages
- Complete resort information

### Dependencies
- Django 5.2.6
- Pillow (for image handling)
- Requests 2.31.0 (for Docker health checks)
- Bootstrap 5.3.2 (CDN)
- Font Awesome 6.0 (CDN)
- Google Fonts (Poppins, Playfair Display)

### Features Implemented
- Responsive design with Bootstrap 5
- Modern CSS animations and hover effects
- Contact form with validation
- Admin interface for content management
- Image placeholders for all content
- Gallery filtering by category
- Room booking interface (frontend ready)
- Newsletter subscription (frontend ready)

### Docker Setup (docker branch)

The project includes Docker support in the `docker` branch:

```bash
# Switch to docker branch
git checkout docker

# Run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop containers
docker-compose down
```

**Docker Features:**
- Multi-stage build optimized for Python/Django
- Automatic database migrations and sample data population
- Health checks for container monitoring
- Volume mounts for persistent data
- Environment variable configuration
- Non-root user for security
- Support for both SQLite (development) and PostgreSQL (production)

### Deployment Considerations
- Configure `ALLOWED_HOSTS` in settings.py or via environment variables
- Set `DEBUG = False` for production
- Configure proper database (PostgreSQL/MySQL) for production
- Set up proper static file serving
- Configure email backend for contact form
- Add SSL certificate for HTTPS
- Use Docker for consistent deployment across environments
