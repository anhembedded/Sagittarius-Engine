from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext


@dataclass
class ExtensionDescriptor:
    """
    @brief Metadata describing an engine extension.
    """

    name: str
    version: str = "1.0.0"
    dependencies: list[str] = field(default_factory=list)
    optional_dependencies: list[str] = field(default_factory=list)
    enabled: bool = True
    priority: int = 0
    author: str = ""
    description: str = ""


class IExtension(ABC):
    """Interface for Sagittarius Engine Extensions."""

    @property
    def descriptor(self) -> ExtensionDescriptor:
        """
        @brief Return the extension descriptor. Defaults to class name and attributes.
        """
        deps = getattr(self, "dependencies", [])
        opt_deps = getattr(self, "optional_dependencies", [])
        prio = getattr(self, "priority", 0)
        enabled = getattr(self, "enabled", True)
        return ExtensionDescriptor(
            name=self.__class__.__name__,
            dependencies=deps if isinstance(deps, list) else [],
            optional_dependencies=opt_deps if isinstance(opt_deps, list) else [],
            priority=prio if isinstance(prio, int) else 0,
            enabled=enabled if isinstance(enabled, bool) else True,
        )


    @abstractmethod
    def register(self, context: "EngineContext") -> None:
        """
        @brief Called first when the extension is registered to bind dependencies.
        @param context The EngineContext instance.
        """
        ...

    @abstractmethod
    def boot(self, context: "EngineContext") -> None:
        """
        @brief Called after all extensions have been registered to trigger startup logic.
        @param context The EngineContext instance.
        """
        ...

    @abstractmethod
    def shutdown(self, context: "EngineContext") -> None:
        """
        @brief Called when the engine is stopping to release resources.
        @param context The EngineContext instance.
        """
        ...

    def initialize(self, context: "EngineContext") -> None:
        """
        @brief Orchestrator initialization step. Defaults to calling register.
        """
        self.register(context)

    def start(self, context: "EngineContext") -> None:
        """
        @brief Orchestrator start step. Defaults to calling boot.
        """
        self.boot(context)

    def stop(self, context: "EngineContext") -> None:
        """
        @brief Orchestrator stop step. Defaults to calling shutdown.
        """
        self.shutdown(context)

    def dispose(self, context: "EngineContext") -> None:
        """
        @brief Orchestrator cleanup/release step. Defaults to no-op.
        """
        pass
