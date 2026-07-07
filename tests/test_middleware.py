from src.core import MiddlewarePipeline
from src.interfaces import IMiddleware


class DummyMiddleware(IMiddleware):
    def __init__(self, name: str, tracer: list):
        self.name = name
        self.tracer = tracer

    def process(self, cmd_or_query, data_transfer_obj, next_handler):
        self.tracer.append(f"{self.name}_start")
        result = next_handler()
        self.tracer.append(f"{self.name}_end")
        return result


def test_middleware_pipeline_execution_order():
    pipeline = MiddlewarePipeline()
    tracer = []

    pipeline.add(DummyMiddleware("mw1", tracer))
    pipeline.add(DummyMiddleware("mw2", tracer))

    def final_handler():
        tracer.append("final")
        return "result"

    result = pipeline.execute("cmd", "data_transfer_obj", final_handler)

    assert result == "result"
    assert tracer == ["mw1_start", "mw2_start", "final", "mw2_end", "mw1_end"]

def test_transaction_middleware_commits_on_success():
    from src.middleware.transaction_middleware import TransactionMiddleware
    from src.interfaces import IContainer, ISession
    from unittest.mock import MagicMock

    mock_container = MagicMock(spec=IContainer)
    mock_session = MagicMock(spec=ISession)
    mock_container.resolve.return_value = mock_session

    middleware = TransactionMiddleware(mock_container)

    def next_handler():
        return "success"

    result = middleware.process(None, None, next_handler)

    assert result == "success"
    mock_session.commit.assert_called_once()
    mock_session.rollback.assert_not_called()

def test_transaction_middleware_rollbacks_on_exception():
    from src.middleware.transaction_middleware import TransactionMiddleware
    from src.interfaces import IContainer, ISession
    from unittest.mock import MagicMock
    import pytest

    mock_container = MagicMock(spec=IContainer)
    mock_session = MagicMock(spec=ISession)
    mock_container.resolve.return_value = mock_session

    middleware = TransactionMiddleware(mock_container)

    def next_handler():
        raise RuntimeError("Command failed")

    with pytest.raises(RuntimeError, match="Command failed"):
        middleware.process(None, None, next_handler)

    mock_session.rollback.assert_called_once()
    mock_session.commit.assert_not_called()
