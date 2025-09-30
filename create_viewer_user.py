#!/usr/bin/env python
"""
Script to create a test viewer user for testing permissions.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')
django.setup()

from django.contrib.auth.models import User
from backoffice.models import UserProfile


def create_viewer_user():
    """Create a test viewer user"""
    print("Creating test viewer user...")
    
    # Create viewer user
    user, created = User.objects.get_or_create(
        username='viewer_test',
        defaults={
            'email': 'viewer@banbas.local',
            'first_name': 'Test',
            'last_name': 'Viewer',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('viewer123')
        user.save()
        print(f"✓ Viewer user created: {user.username}")
    else:
        user.set_password('viewer123')
        user.save()
        print(f"✓ Viewer user updated: {user.username}")
    
    # Create viewer profile
    profile, profile_created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'viewer'}
    )
    
    if profile_created:
        print(f"✓ Viewer profile created with role: {profile.role}")
    else:
        profile.role = 'viewer'
        profile.save()
        print(f"✓ Viewer profile updated with role: {profile.role}")
    
    print("\n" + "="*50)
    print("VIEWER USER CREATED!")
    print("VIEWER LOGIN:")
    print("  Username: viewer_test")
    print("  Password: viewer123")
    print("  URL: http://localhost:8000/_internal/")
    print("  Permissions: Read-only access to reservations and inquiries")
    print("="*50)


if __name__ == '__main__':
    create_viewer_user()