"""Unit tests for TASK-010: Async Lifecycle Support in IExtension."""

import asyncio
import threading
from unittest.mock import MagicMock
from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.interfaces.i_engine_context import IEngineContext


class AsyncBootExtension(IExtension):
    """Extension that overrides boot_async to track async boot calls."""

    def __init__(self) -> None:
        self.sync_boot_called = False
        self.async_boot_called = False
        self.async_shutdown_called = False

    def register(self, context: IEngineContext) -> None:
        pass

    def boot(self, context: IEngineContext) -> None:
        self.sync_boot_called = True

    def shutdown(self, context: IEngineContext) -> None:
        pass

    async def boot_async(self, context: IEngineContext) -> None:
        await asyncio.sleep(0)  # Simulate I/O wait
        self.async_boot_called = True

    async def shutdown_async(self, context: IEngineContext) -> None:
        await asyncio.sleep(0)
        self.async_shutdown_called = True


class SyncOnlyExtension(IExtension):
    """Extension that does NOT override async hooks — uses default no-op."""

    def register(self, context: IEngineContext) -> None:
        pass

    def boot(self, context: IEngineContext) -> None:
        pass

    def shutdown(self, context: IEngineContext) -> None:
        pass


class TestAsyncLifecycle:
    def test_default_boot_async_is_noop(self) -> None:
        """base IExtension.boot_async must be a coroutine that does nothing."""
        ext = SyncOnlyExtension()
        ctx = MagicMock(spec=IEngineContext)
        # Should run without error and return None
        result = asyncio.run(ext.boot_async(ctx))
        assert result is None

    def test_default_shutdown_async_is_noop(self) -> None:
        """base IExtension.shutdown_async must be a coroutine that does nothing."""
        ext = SyncOnlyExtension()
        ctx = MagicMock(spec=IEngineContext)
        result = asyncio.run(ext.shutdown_async(ctx))
        assert result is None

    def test_overridden_boot_async_runs_on_event_loop(self) -> None:
        """boot_async override must be awaitable and update state."""
        ext = AsyncBootExtension()
        ctx = MagicMock(spec=IEngineContext)
        asyncio.run(ext.boot_async(ctx))
        assert ext.async_boot_called is True

    def test_overridden_shutdown_async_runs_on_event_loop(self) -> None:
        """shutdown_async override must be awaitable and update state."""
        ext = AsyncBootExtension()
        ctx = MagicMock(spec=IEngineContext)
        asyncio.run(ext.shutdown_async(ctx))
        assert ext.async_shutdown_called is True

    def test_sync_only_extension_does_not_override_boot_async(self) -> None:
        """SyncOnlyExtension should use the base class boot_async (no override detection)."""
        assert SyncOnlyExtension.boot_async is IExtension.boot_async

    def test_async_extension_overrides_boot_async(self) -> None:
        """AsyncBootExtension should be detected as having an override."""
        assert AsyncBootExtension.boot_async is not IExtension.boot_async

    def test_boot_async_does_not_block_main_thread(self) -> None:
        """Verify boot_async can run on background loop without blocking test thread."""
        ext = AsyncBootExtension()
        ctx = MagicMock(spec=IEngineContext)

        loop = asyncio.new_event_loop()
        thread = threading.Thread(target=loop.run_forever, daemon=True)
        thread.start()

        future = asyncio.run_coroutine_threadsafe(ext.boot_async(ctx), loop)
        future.result(timeout=3.0)  # Should complete quickly

        assert ext.async_boot_called is True

        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=2.0)
