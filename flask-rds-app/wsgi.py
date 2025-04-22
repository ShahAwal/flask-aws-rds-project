from app import create_app

app = create_app()

# Gunicorn will look for the 'app' callable in this file
# You might need this if running 'gunicorn wsgi:app'
