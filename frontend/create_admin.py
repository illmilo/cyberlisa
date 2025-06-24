import os
import django
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

def create_admin_user():
    User = get_user_model()
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.getenv('ADMIN_PASSWORD', 'securepassword123')
    
    if not User.objects.filter(email=admin_email).exists():
        User.objects.create_superuser(
            username=admin_email.split('@')[0],
            email=admin_email,
            password=admin_password
        )
        print(f"✅ Admin user {admin_email} created successfully!")
    else:
        print("ℹ️ Admin user already exists")

if __name__ == "__main__":
    create_admin_user()