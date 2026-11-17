# Deploying IntelliSoft Innovations on PythonAnywhere

## 1. Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Ready for PythonAnywhere deployment"
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## 2. Clone & Set Up Virtual Environment on PythonAnywhere
Open a **Bash console** on PythonAnywhere and run:
```bash
git clone https://github.com/<your-username>/<your-repo>.git intellisoft
cd intellisoft
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure `.env`
```bash
cp .env.example .env
nano .env
```
Set your production values (replace `yourusername` with your PythonAnywhere username):
```env
DJANGO_SECRET_KEY=<generate-a-50-char-random-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
```
You can generate a secret key quickly with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 4. Run Migrations, Seed Data & Collect Static Files
```bash
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 5. Configure the PythonAnywhere Web Tab
1. Go to **Web** -> **Add a new web app** -> **Manual configuration** -> **Python 3.12**.
2. **Virtualenv**: Set path to `/home/yourusername/intellisoft/venv`.
3. **Static files** mappings:
   - URL: `/static/` -> Directory: `/home/yourusername/intellisoft/staticfiles`
   - URL: `/media/` -> Directory: `/home/yourusername/intellisoft/media`
4. **WSGI configuration file**: Replace its contents with:
```python
import os
import sys

path = '/home/yourusername/intellisoft'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intellisoft.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
5. Click **Reload yourusername.pythonanywhere.com**.
