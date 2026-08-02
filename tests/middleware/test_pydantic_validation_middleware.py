import pytest
from unittest.mock import patch
from pydantic import BaseModel

from sagittarius_engine.middleware.pydantic_validation_middleware import (
    PydanticValidationMiddleware,
)


class MyDTO(BaseModel):
    name: str
    age: int


class DummyObj:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class DummyCommand:
    pass


def test_init_raises_import_error_when_pydantic_missing():
    with patch(
        "sagittarius_engine.middleware.pydantic_validation_middleware.BaseModel", None
    ):
        with pytest.raises(ImportError, match="pydantic is not installed"):
            PydanticValidationMiddleware(container=None)


def test_successful_validation_with_dict():
    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = MyDTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = {"name": "Alice", "age": 30}
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"


def test_successful_validation_with_none():
    class OptionalDTO(BaseModel):
        name: str = "default"
        age: int = 0

    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = OptionalDTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    result = middleware.process(DummyCommand(), None, next_handler)

    assert called
    assert result == "success"


def test_successful_validation_with_model_instance():
    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = MyDTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = MyDTO(name="Bob", age=25)
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"


def test_successful_validation_with_object_dict():
    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = MyDTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = DummyObj("Charlie", 40)
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"


def test_validation_failure_raises_value_error():
    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = MyDTO

    def next_handler():
        pass

    data = {"name": "Dave"}  # Missing age

    with pytest.raises(ValueError, match="Validation failed for DummyCommand"):
        middleware.process(DummyCommand(), data, next_handler)


def test_v1_fallback_dict():
    # Create a mock V1 model class
    class V1DTO:
        def __init__(self, **kwargs):
            self.name = kwargs.get("name")
            self.age = kwargs.get("age")
            if not self.name or not self.age:
                pass

        def __eq__(self, other):
            return self.name == other.name and self.age == other.age

    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = V1DTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = {"name": "Eve", "age": 22}
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"


def test_v1_fallback_none():
    class V1DTO:
        def __init__(self):
            self.name = "default"
            self.age = 0

    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = V1DTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    result = middleware.process(DummyCommand(), None, next_handler)

    assert called
    assert result == "success"


def test_v1_fallback_object_dict():
    class V1DTO:
        def __init__(self, **kwargs):
            self.name = kwargs.get("name")
            self.age = kwargs.get("age")

    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = V1DTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = DummyObj("Frank", 50)
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"


def test_v1_fallback_model_instance():
    class V1DTO:
        def __init__(self, **kwargs):
            self.name = kwargs.get("name")
            self.age = kwargs.get("age")

    middleware = PydanticValidationMiddleware(container=None)
    middleware.model_class = V1DTO
    called = False

    def next_handler():
        nonlocal called
        called = True
        return "success"

    data = V1DTO(name="Grace", age=33)
    result = middleware.process(DummyCommand(), data, next_handler)

    assert called
    assert result == "success"
