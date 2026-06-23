import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, jsonify, request
from src.core import App, IEventBus
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.modules.logger_module import LoggerModule
from example.simple_ui.modules.hello_module import HelloModule
from example.simple_ui.application.get_hello_query import GetHelloQuery

flask_app = Flask(__name__)

container = StdLibContainer()
event_bus = MemoryEventBus()
core_app = App(container, event_bus)

core_app.use(LoggerModule())
core_app.use(HelloModule())
core_app.boot()

@flask_app.route('/')
def index():
    name = request.args.get('name', 'World')
    result = core_app.query(GetHelloQuery, name)
    return jsonify({"message": result})

if __name__ == "__main__":
    flask_app.run(port=5000)
