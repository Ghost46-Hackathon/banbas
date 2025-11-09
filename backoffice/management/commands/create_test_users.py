from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from backoffice.models import UserProfile


class Command(BaseCommand):
    help = 'Create test users for the backoffice system'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating test users for Banbas Resort backoffice...'))

        # Test users data
        test_users = [
            {
                'username': 'banbas_admin',
                'email': 'admin@banbasresort.com',
                'password': 'admin123',
                'first_name': 'Banbas',
                'last_name': 'Admin',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'agent_test',
                'email': 'agent@banbasresort.com',
                'password': 'agent123',
                'first_name': 'Test',
                'last_name': 'Agent',
                'role': 'agent',
                'is_staff': False,
                'is_superuser': False
            },
            {
                'username': 'viewer_test',
                'email': 'viewer@banbasresort.com',
                'password': 'viewer123',
                'first_name': 'Test',
                'last_name': 'Viewer',
                'role': 'viewer',
                'is_staff': False,
                'is_superuser': False
            }
        ]

        for user_data in test_users:
            # Create or get the user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['is_staff'],
                    'is_superuser': user_data['is_superuser']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'✓ Created user: {user.username}')
            else:
                # Update password if user exists
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'✓ Updated password for existing user: {user.username}')

            # Create or update UserProfile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': user_data['role']}
            )
            
            if not profile_created:
                # Update role if profile exists
                profile.role = user_data['role']
                profile.save()
                self.stdout.write(f'✓ Updated role for {user.username}: {profile.get_role_display()}')
            else:
                self.stdout.write(f'✓ Created profile for {user.username}: {profile.get_role_display()}')

        self.stdout.write(self.style.SUCCESS('\nTest users created successfully!'))
        self.stdout.write(self.style.WARNING('\nTest User Credentials:'))
        self.stdout.write('Admin: banbas_admin / admin123')
        self.stdout.write('Agent: agent_test / agent123')
        self.stdout.write('Viewer: viewer_test / viewer123')
        self.stdout.write(self.style.SUCCESS('\nYou can now access the backoffice at: http://127.0.0.1:8000/_internal/login/'))



