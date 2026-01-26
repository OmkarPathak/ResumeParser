
import os
import sys
import time
import threading
import webview
import socket
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_parser.settings')

if getattr(sys, 'frozen', False):
    import django
    from django.conf import settings
    
    django.setup()
    # Override STATIC_ROOT to point to the temporary directory where PyInstaller extracts files
    # The 'parser_app/static' path matches what is in ResumeParser.spec datas
    settings.STATIC_ROOT = os.path.join(sys._MEIPASS, 'parser_app', 'static')


def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def start_server(port):
    application = get_wsgi_application()
    # Using wsgiref for simplicity in this bundled env. 
    # For production with high load, one might bundle waitress or similar, 
    # but for a local desktop app, simple_server is usually sufficient for single user.
    httpd = make_server('127.0.0.1', port, application)
    httpd.serve_forever()

def start_webview(port):
    webview.create_window('Resume Parser', f'http://127.0.0.1:{port}')
    webview.start()

if __name__ == '__main__':
    port = get_free_port()
    
    # Start Django in a background thread
    t = threading.Thread(target=start_server, args=(port,))
    t.daemon = True
    t.start()

    # Give Django a moment to start (optional, but good for stability)
    time.sleep(1)

    # Start the native window
    start_webview(port)
