# TASK-003: End-to-End Async Pipeline Support

- **Status**: 📝 Planned (Backlog)
- **Priority**: P1 - High
- **Category**: Core Engine / Trading Domain

---

## 🎯 Goal
Upgrade `ICommand`, `IQuery`, and `MiddlewarePipeline` to support native asynchronous execution (`async`/`await`), allowing high-throughput I/O bound applications (such as Trading Bots and WebSocket clients) to run without blocking worker threads.

---

## 📐 Key Enhancements
1. **Async Command & Query Handlers**: Update `App.dispatch()` to natively resolve and await async coroutine handlers.
2. **Async Middleware Pipeline**: Support `async def handle(self, req, next_fn)` in middleware.
3. **Trading Bot Async Adapter**: Provide non-blocking WebSocket data ingestion pipeline.

---

## 📋 Implementation Checklist
- [ ] Support async coroutines in `Dispatcher.dispatch()`.
- [ ] Add `IAsyncMiddleware` interface in `sagittarius_engine.interfaces`.
- [ ] Update `MiddlewarePipeline` to support async middleware chains.
- [ ] Add unit tests in `tests/test_async_pipeline.py`.
