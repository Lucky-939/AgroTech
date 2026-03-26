#!/usr/bin/env python
import os
import sys

def main():
    # SAFETY GUARD: Ensure we are using the virtual environment with TensorFlow
    try:
        import tensorflow
    except ImportError:
        print("\n" + "!"*60)
        print("CRITICAL ERROR: TENSORFLOW NOT FOUND!")
        print("You are running 'python manage.py' (System Python 3.14).")
        print("PLEASE USE THIS COMMAND INSTEAD:")
        print(".\\venv\\Scripts\\python manage.py runserver")
        print("!"*60 + "\n")
        sys.exit(1)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
