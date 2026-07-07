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
