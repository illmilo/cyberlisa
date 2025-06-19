import os
from django.core.management import execute_from_command_line

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Run migrations
execute_from_command_line(['manage.py', 'migrate'])

# Create superuser if needed
if not os.environ.get('ADMIN_CREATED'):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='securepassword123'
        )
        os.environ['ADMIN_CREATED'] = 'True'