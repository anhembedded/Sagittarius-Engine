## 🧵 Async & Đa luồng trong framework: Hiện trạng và hướng đi

Framework hiện tại (Phase 2) có EventBus **đồng bộ hoàn toàn**: khi bạn gọi `emit`, tất cả handler được gọi tuần tự ngay trên cùng luồng gọi. Điều này đơn giản, dễ hiểu, nhưng chưa đủ cho các kịch bản phức tạp mà bạn đề cập. Mình sẽ giải đáp từng ý.

---

### 1. Event bus bất đồng bộ sẽ dựa trên cái gì?

Có thể triển khai trên một trong ba nền tảng (theo mức độ phức tạp tăng dần):

| Cách | Mô tả | Dùng khi |
|------|-------|----------|
| **Thread pool** | Mỗi handler chạy trong một worker thread (dùng `concurrent.futures.ThreadPoolExecutor`). Event bus gửi task vào executor. | Handler có thể block nhẹ (I/O), không cần async/await. |
| **asyncio** | Handler là async function, event bus dùng `asyncio.create_task` hoặc `await` theo loạt. Cần vòng lặp sự kiện. | Muốn tận dụng async/await, không blocking, cùng process. |
| **Message Queue (broker)** | Event được gửi qua Redis, RabbitMQ, Kafka. Handler chạy ở bất kỳ process/máy nào subscribe. | Cần độ tin cậy cao, liên process, microservices. |

Framework có thể hỗ trợ cả ba bằng cách cung cấp các adapter khác nhau của `IEventBus`: `AsyncEventBus`, `ThreadPoolEventBus`, `RedisEventBus`...

---

### 2. Một module muốn chạy trên thread riêng thì sao?

Bạn có thể cho module tự tạo thread trong `boot()`:

```python
import threading

class BackgroundModule(BaseModule):
    def boot(self, app):
        self.thread = threading.Thread(target=self._run, args=(app,), daemon=True)
        self.thread.start()

    def _run(self, app):
        while True:
            # Làm việc gì đó, thỉnh thoảng emit event
            app.event_bus.emit('background.task_done', data)
```

Tuy nhiên, **EventBus hiện tại không thread‑safe** (dict handler có thể bị thay đổi đồng thời). Cần giải quyết:
- Bảo vệ `_handlers` bằng `threading.Lock`.
- Đảm bảo handler không được thay đổi khi đang duyệt (có thể snapshot danh sách).

---

### 3. Một task chạy trên thread riêng rồi report event thì sao?

Tương tự, task đó gọi `event_bus.emit(...)`. Nếu EventBus được bảo vệ thread‑safe thì hoạt động. Nhưng cần lưu ý: **handler của event đó sẽ chạy trên luồng của task**, không phải luồng chính. Nếu handler cập nhật UI (ví dụ Tkinter), sẽ gặp lỗi. Giải pháp:
- Dùng cơ chế dispatch an toàn: tất cả handler luôn chạy trên cùng một luồng (main thread) bằng cách đưa event vào một queue và main thread xử lý (giống như message loop của Win32, Qt).
- Hoặc đánh dấu handler nào chạy trên thread nào.

---

### 4. Một module chạy như một service trên process riêng thì sao?

Lúc này, bạn không thể dùng chung `EventBus` trong bộ nhớ. Cần một **EventBus liên process** (IPC). Có thể làm:
- Dùng `multiprocessing.Queue` hoặc `Pipe` để gửi event giữa process cha và process con.
- Hoặc dùng một message broker bên ngoài (Redis, RabbitMQ). Framework cung cấp `IEventBus` adapter cho broker đó.

Module process con sẽ có container riêng, đăng ký handler riêng, và lắng nghe event từ broker.

---

### 5. Framework hiện thiếu gì để làm những điều trên?

Framework chưa có:
- **Thread‑safety** cho `EventBus` và `Container` (các dict cần lock).
- **Async/await support** (`IAsyncCommand`, `IAsyncQuery`, `IAsyncEventBus`).
- **Khả năng dispatch handler trên một luồng cụ thể** (ví dụ main thread).
- **Event bus cho nhiều process** (IPC adapter).
- **Cấu hình execution strategy**: cho phép chọn chạy handler đồng bộ, bất đồng bộ (thread), hay qua message queue.

---

### 🎯 Định hướng cho Phase 3.4 (Async & Concurrency)

Mình đề xuất làm từng bước nhỏ:
1. **Thêm thread‑safety cơ bản** cho `MemoryEventBus` (lock khi đọc/ghi handler).
2. **Tạo `ThreadPoolEventBus`** kế thừa `IEventBus`, dùng executor để chạy handler trong thread pool.
3. **Tạo `IAsyncEventBus`** với `async emit/on`, triển khai bằng asyncio.
4. **Cung cấp adapter cho Redis/RabbitMQ** (cho liên process sau này).

Như vậy, framework sẽ dần đáp ứng được mọi kịch bản từ đơn giản (đồng bộ) đến phức tạp (đa tiến trình, microservices).


1. **Thêm thread‑safety cơ bản** cho `MemoryEventBus` (lock khi đọc/ghi handler).
2. **Tạo `ThreadPoolEventBus`** kế thừa `IEventBus`, dùng executor để chạy handler trong thread pool.
3. **Tạo `IAsyncEventBus`** với `async emit/on`, triển khai bằng asyncio.
4. Tạo BaseEvent