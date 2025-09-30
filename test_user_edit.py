#!/usr/bin/env python
"""
Test script to verify user edit functionality is working correctly.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from backoffice.models import UserProfile


def test_user_edit():
    """Test user edit functionality"""
    print("🧪 Testing User Edit Functionality")
    print("=" * 50)
    
    client = Client()
    
    # Login as admin
    login_success = client.login(username='banbas_admin', password='admin123')
    if not login_success:
        print("❌ Failed to login as admin")
        return
    
    print("✅ Logged in as admin")
    
    # Test cases
    test_cases = [
        {
            'user_id': 999,
            'description': 'Non-existent user ID',
            'expected_status': 302,  # Should redirect
            'should_fail': True
        },
        {
            'user_id': 1,  # Usually the first superuser
            'description': 'Existing user (may not have profile)',
            'expected_status': [302, 200],  # Could redirect or show page
            'should_fail': False
        }
    ]
    
    # Get a valid user ID for testing
    try:
        valid_user = User.objects.filter(userprofile__isnull=False).first()
        if valid_user:
            test_cases.append({
                'user_id': valid_user.id,
                'description': f'Valid user with profile ({valid_user.username})',
                'expected_status': 200,
                'should_fail': False
            })
    except Exception as e:
        print(f"⚠️  Could not find valid user: {e}")
    
    # Test each case
    for case in test_cases:
        print(f"\n🧪 Testing: {case['description']}")
        
        try:
            url = f"/_internal/users/{case['user_id']}/edit/"
            response = client.get(url)
            
            status = response.status_code
            expected = case['expected_status']
            
            # Check if status is expected
            if isinstance(expected, list):
                status_ok = status in expected
            else:
                status_ok = status == expected
            
            if status_ok:
                print(f"   ✅ Status {status}: OK")
                if status == 200:
                    print("   ✅ Page loaded successfully")
                elif status == 302:
                    print(f"   ✅ Redirected to: {response.get('Location', 'unknown')}")
            else:
                print(f"   ❌ Status {status}: Expected {expected}")
                
        except Exception as e:
            if case['should_fail']:
                print(f"   ⚠️  Expected error: {e}")
            else:
                print(f"   ❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 User Edit Test Complete")
    
    # Additional check: ensure no AttributeError about '_meta'
    print("\n🔍 Checking for the specific error that was reported...")
    try:
        # Try to access a user that should work
        admin_user = User.objects.get(username='banbas_admin')
        url = f"/_internal/users/{admin_user.id}/edit/"
        response = client.get(url)
        
        if response.status_code in [200, 302]:
            print("✅ No '_meta' AttributeError detected")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error still exists: {e}")


if __name__ == '__main__':
    test_user_edit()