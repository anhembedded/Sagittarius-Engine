from typing import Any
from collections.abc import Callable
from pydantic import BaseModel, Field
from sagittarius_engine.interfaces import IMiddleware
from sagittarius_engine.middleware.pydantic_validation_middleware import PydanticValidationMiddleware


class AddStudentPydanticDTO(BaseModel):
    student_id: str = Field(min_length=3, max_length=10, description="ID must be 3-10 chars")
    full_name: str = Field(min_length=1, description="Name cannot be empty")
    age: int = Field(gt=0, lt=150, description="Age must be 1 to 149")
    gender: str = Field(min_length=1, description="Gender cannot be empty")
    major: str = Field(min_length=1, description="Major cannot be empty")
    gpa: float = Field(ge=0.0, le=4.0, description="GPA must be 0.0 to 4.0")


class StudentValidationMiddleware(IMiddleware):
    def __init__(self) -> None:
        self.validator = PydanticValidationMiddleware(AddStudentPydanticDTO)

    def process(
        self, cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable[[], Any]
    ) -> Any:
        if cmd_or_query.__class__.__name__ == "AddStudentCommandHandler":
            # Map object __dict__ to validate AddStudentCommand properties
            if hasattr(data_transfer_obj, "__dict__"):
                dto_dict = data_transfer_obj.__dict__
            else:
                dto_dict = data_transfer_obj
            return self.validator.process(cmd_or_query, dto_dict, next_handler)
        return next_handler()
