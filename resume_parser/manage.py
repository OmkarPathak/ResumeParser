#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Check if running as a standalone executable (frozen) and no args provided
    if getattr(sys, 'frozen', False) and len(sys.argv) == 1:
        # Running in double-click mode
        import threading
        import time
        import webbrowser

        def open_browser():
            time.sleep(2)  # Wait for server to start
            webbrowser.open('http://127.0.0.1:8000')

        threading.Thread(target=open_browser).start()
        
        # Append arguments to start server
        sys.argv.extend(['runserver', '--noreload', '0.0.0.0:8000'])

    execute_from_command_line(sys.argv)
