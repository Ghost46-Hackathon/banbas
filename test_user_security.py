#!/usr/bin/env python
"""
Security test script to verify user management access controls.
This script tests that Agent role users cannot access user management functionality.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banbas_resort.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from backoffice.models import UserProfile


def test_user_management_security():
    """Test that agent users cannot access user management"""
    print("=" * 60)
    print("TESTING USER MANAGEMENT SECURITY")
    print("=" * 60)
    
    client = Client()
    
    # Test cases for different user roles
    test_cases = [
        {
            'role': 'agent',
            'should_access': False,
            'description': 'Agent user (should be BLOCKED)'
        },
        {
            'role': 'viewer', 
            'should_access': False,
            'description': 'Viewer user (should be BLOCKED)'
        },
        {
            'role': 'admin',
            'should_access': True,
            'description': 'Admin user (should have ACCESS)'
        }
    ]
    
    # URLs to test for user management (admin only)
    user_management_urls = [
        ('user_list', 'User List Page'),
        ('user_create', 'User Create Page'),
    ]
    
    # URLs to test for viewer access (should be allowed)
    viewer_allowed_urls = [
        ('reservation_list', 'Reservation List Page'),
        ('inquiry_list', 'Inquiry List Page'),
        ('analytics', 'Analytics Page'),
    ]
    
    # URLs to test for agent/admin only (should be blocked for viewers)
    agent_only_urls = [
        ('reservation_create', 'Create Reservation Page'),
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing {test_case['description']}")
        print("-" * 50)
        
        # Find a user with this role
        try:
            profile = UserProfile.objects.filter(role=test_case['role']).first()
            if not profile:
                print(f"❌ No {test_case['role']} user found in system")
                continue
                
            user = profile.user
            print(f"   User: {user.username} (Role: {profile.get_role_display()})")
            
            # Login as this user
            login_success = False
            passwords = ['admin123', 'agent123', 'viewer123']
            
            for password in passwords:
                login_success = client.login(username=user.username, password=password)
                if login_success:
                    break
            
            if not login_success:
                print(f"   ❌ Could not login as {user.username}")
                continue
                
            print(f"   ✅ Successfully logged in as {user.username}")
            
            # Test user management URLs (admin only)
            print(f"   Testing User Management Access:")
            for url_name, description in user_management_urls:
                try:
                    url = reverse(f'backoffice:{url_name}')
                    response = client.get(url)
                    
                    # Check response
                    if test_case['role'] == 'admin':
                        # Admin should get 200
                        if response.status_code == 200:
                            print(f"     ✅ {description}: ACCESS GRANTED (Expected)")
                        else:
                            print(f"     ❌ {description}: ACCESS DENIED (Unexpected) - Status: {response.status_code}")
                    else:
                        # Agent/Viewer should be redirected or get 403
                        if response.status_code in [302, 403]:
                            print(f"     ✅ {description}: ACCESS BLOCKED (Expected) - Status: {response.status_code}")
                        elif response.status_code == 200:
                            print(f"     ❌ {description}: ACCESS GRANTED (Security Issue!) - Status: {response.status_code}")
                        else:
                            print(f"     ⚠️  {description}: Unexpected response - Status: {response.status_code}")
                            
                except Exception as e:
                    print(f"     ❌ {description}: Error testing - {e}")
            
            # Test viewer-allowed URLs (all roles should access)
            print(f"   Testing General Access:")
            for url_name, description in viewer_allowed_urls:
                try:
                    url = reverse(f'backoffice:{url_name}')
                    response = client.get(url)
                    
                    if response.status_code == 200:
                        print(f"     ✅ {description}: ACCESS GRANTED (Expected for all roles)")
                    else:
                        print(f"     ❌ {description}: ACCESS DENIED (Unexpected) - Status: {response.status_code}")
                        
                except Exception as e:
                    print(f"     ❌ {description}: Error testing - {e}")
            
            # Test agent-only URLs (viewers should be blocked)
            print(f"   Testing Agent-Only Access:")
            for url_name, description in agent_only_urls:
                try:
                    url = reverse(f'backoffice:{url_name}')
                    response = client.get(url)
                    
                    if test_case['role'] in ['agent', 'admin']:
                        # Agent/Admin should get 200
                        if response.status_code == 200:
                            print(f"     ✅ {description}: ACCESS GRANTED (Expected for {test_case['role']})")
                        else:
                            print(f"     ❌ {description}: ACCESS DENIED (Unexpected) - Status: {response.status_code}")
                    else:
                        # Viewer should be blocked
                        if response.status_code in [302, 403]:
                            print(f"     ✅ {description}: ACCESS BLOCKED (Expected for viewer) - Status: {response.status_code}")
                        elif response.status_code == 200:
                            print(f"     ❌ {description}: ACCESS GRANTED (Security Issue for viewer!) - Status: {response.status_code}")
                        else:
                            print(f"     ⚠️  {description}: Unexpected response - Status: {response.status_code}")
                            
                except Exception as e:
                    print(f"     ❌ {description}: Error testing - {e}")
            
            # Logout
            client.logout()
            
        except Exception as e:
            print(f"❌ Error testing {test_case['role']} user: {e}")
    
    print("\n" + "=" * 60)
    print("SECURITY TEST COMPLETED")
    print("=" * 60)


def show_user_roles():
    """Display all users and their roles"""
    print("\n📋 CURRENT USER ROLES:")
    print("-" * 40)
    
    users = User.objects.all()
    for user in users:
        try:
            profile = user.userprofile
            role_display = profile.get_role_display()
            can_edit = profile.can_edit_reservations()
            can_view_revenue = profile.can_view_revenue()
            
            print(f"👤 {user.username}")
            print(f"   Role: {role_display}")
            print(f"   Can edit reservations: {can_edit}")
            print(f"   Can view revenue: {can_view_revenue}")
            print(f"   Active: {user.is_active}")
            print()
        except UserProfile.DoesNotExist:
            print(f"👤 {user.username} (No profile)")
            print()


if __name__ == '__main__':
    print("🔐 BANBAS RESORT - USER MANAGEMENT SECURITY TEST")
    
    show_user_roles()
    test_user_management_security()
    
    print("\n💡 SECURITY SUMMARY:")
    print("   ✅ Agent users should be BLOCKED from user management")
    print("   ✅ Viewer users should be BLOCKED from user management") 
    print("   ✅ Only Admin users should have ACCESS to user management")
    print("   ⚠️  If any Agent/Viewer shows 'ACCESS GRANTED', there's a security issue!")