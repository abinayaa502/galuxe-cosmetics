import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'galuxe_project.settings')
django.setup()

from users.models import User

# Use your preferred email here if you'd like
ADMIN_EMAIL = 'admin@galuxe.com'
ADMIN_PASS = 'admin123'

if not User.objects.filter(email=ADMIN_EMAIL).exists():
    User.objects.create_superuser(ADMIN_EMAIL, ADMIN_PASS)
    print(f"✅ Success: Superuser created ({ADMIN_EMAIL})")
else:
    print("ℹ️ Info: Superuser already exists.")
