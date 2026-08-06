from unittest.mock import MagicMock
from sagittarius_engine.interfaces.i_engine_context import IEngineContext
from sagittarius_engine.extensions.thread_manager.thread_manager_module import (
    ThreadManagerModule,
)


class ConcreteThreadManagerModule(ThreadManagerModule):
    def boot(self, app):
        pass

    def shutdown(self, app):
        pass


def test_thread_manager_module_register():
    module = ConcreteThreadManagerModule()
    context_mock = MagicMock(spec=IEngineContext)
    module.register(context_mock)
