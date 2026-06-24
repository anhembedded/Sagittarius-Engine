import os
import sys
import threading
import time
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.interfaces import IEventBus

from example.simple_ui.modules.user_module import UserModule
from example.simple_ui.adapters.web.app import create_app

def setup_framework() -> App:
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IEventBus, event_bus)
    app.use(UserModule())
    app.boot()
    return app

def run_server(flask_app):
    # Running in debug mode causes issue with thread reloading, so turn it off
    flask_app.run(port=5000, debug=False, use_reloader=False)

def main():
    framework_app = setup_framework()
    flask_app = create_app(framework_app)

    # Start Flask server in a separate thread for testing
    server_thread = threading.Thread(target=run_server, args=(flask_app,))
    server_thread.daemon = True
    server_thread.start()

    # Wait for server to start
    time.sleep(1)

    print("--- Creating users via API ---")
    requests.post('http://127.0.0.1:5000/users', json={'username': 'alice'})
    requests.post('http://127.0.0.1:5000/users', json={'username': 'bob'})

    print("--- Fetching users via API ---")
    response = requests.get('http://127.0.0.1:5000/users')
    print(response.json())

if __name__ == "__main__":
    main()
