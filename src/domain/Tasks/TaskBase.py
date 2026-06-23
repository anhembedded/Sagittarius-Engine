from abc import ABC, abstractmethod
from typing import Any
from Domain.Tasks.task_contextBase import ITaskContext

class AbstractTask(ABC):
    """Base class for all domain tasks.
    
    Tasks are pure domain logic — no dependency on Qt or any UI framework.
    """

    @abstractmethod 
    def run(self, ctx: ITaskContext) -> Any:
        """Execute the task logic.
        
        Args:
            ctx: A ITaskContext instance used to report progress, messages,
                 and check for cancellation.

        Returns:
            Any result value, or None.
        """
        pass
