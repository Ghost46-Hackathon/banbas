#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')
django.setup()

from django.contrib.auth.models import User
from backoffice.models import UserProfile

def create_admin_user():
    # Create admin user
    user, created = User.objects.get_or_create(
        username='banbas_admin',
        defaults={
            'email': 'admin@banbas.local',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        user.set_password('admin123')
        user.save()
        print(f"✓ Admin user created: {user.username}")
    else:
        user.set_password('admin123')
        user.save()
        print(f"✓ Admin user updated: {user.username}")
    
    # Create admin profile
    profile, profile_created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'admin'}
    )
    
    if profile_created:
        print(f"✓ Admin profile created with role: {profile.role}")
    else:
        print(f"✓ Admin profile already exists with role: {profile.role}")

def create_test_agent():
    # Create test agent user
    agent_user, created = User.objects.get_or_create(
        username='agent_test',
        defaults={
            'email': 'agent@banbas.local',
            'first_name': 'Test',
            'last_name': 'Agent'
        }
    )
    
    if created:
        agent_user.set_password('agent123')
        agent_user.save()
        print(f"✓ Agent user created: {agent_user.username}")
    else:
        agent_user.set_password('agent123')
        agent_user.save()
        print(f"✓ Agent user updated: {agent_user.username}")
    
    # Create agent profile
    agent_profile, profile_created = UserProfile.objects.get_or_create(
        user=agent_user,
        defaults={'role': 'agent'}
    )
    
    if profile_created:
        print(f"✓ Agent profile created with role: {agent_profile.role}")
    else:
        print(f"✓ Agent profile already exists with role: {agent_profile.role}")

if __name__ == '__main__':
    print("Setting up Banbas Resort Management System...")
    print("-" * 50)
    
    create_admin_user()
    create_test_agent()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("ADMIN LOGIN:")
    print("  Username: banbas_admin")
    print("  Password: admin123")
    print("  URL: http://localhost:8000/_internal/")
    print("")
    print("AGENT LOGIN:")
    print("  Username: agent_test")
    print("  Password: agent123")
    print("="*50)
    print("\nRun: python manage.py runserver")
