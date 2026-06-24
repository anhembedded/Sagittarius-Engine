# Hướng dẫn sử dụng Framework Sagittarius

Sagittarius là một Python Framework được xây dựng dựa trên nguyên lý **Clean Architecture** và **Domain-Driven Design (DDD)**. Hệ thống có cơ chế phân tách rõ ràng các layer: Domain, Application, Infrastructure và Adapter, thông qua hệ thống **Dependency Injection (DI)** siêu nhẹ và kiến trúc **Event-Driven**.

Mục tiêu cốt lõi: *"Bảo vệ Business Logic (Domain) khỏi các tác động của Framework và công nghệ bên ngoài, đồng thời giữ ứng dụng dễ test và mở rộng."*

---

## 1. Cài đặt Framework

Vì framework chỉ dựa vào thư viện chuẩn (Standard Library) của Python cho core (Trừ khi bạn dùng Adapter như web flask/CLI), cài đặt cực kỳ nhẹ và đơn giản.

Để sử dụng framework trong dự án hiện tại dưới dạng module cài đặt (editable mode) cho việc phát triển:

```bash
pip install -e .
```

---

## 2. Scaffold: Tạo dự án mới

Framework cung cấp công cụ tự động sinh cấu trúc thư mục chuẩn Clean Architecture:

```bash
python -m src.scaffold my_app
```

Cấu trúc tạo ra (bên trong `my_app/`) bao gồm:
- `domain/`: Chứa các thực thể, interface cốt lõi của bài toán.
- `application/`: Chứa Use Cases (Commands / Queries).
- `infrastructure/`: Implement các interfaces (Database, API, Message Broker).
- `adapters/`: UI, Web Controllers, CLI entry.
- `modules/`: Nơi đóng gói tính năng để framework tự động load.
- `main.py`: Điểm khởi chạy (Composition Root).

---

## 3. Tạo Module đầu tiên

Trong framework, **Module** (`IModule`) là đơn vị lắp ghép các tính năng. Mỗi Module sẽ cung cấp các service vào DI Container hoặc đăng ký Event listeners.

Ví dụ tạo một `UserModule` trong file `modules/user_module.py`:

```python
from src.interfaces import IModule, IContainer, IEventBus

class UserModule(IModule):
    def register(self, container: IContainer) -> None:
        # Đăng ký các repository, service vào Container tại đây.
        # Ví dụ: container.singleton(IUserRepository, MemoryUserRepository())
        pass

    def boot(self, event_bus: IEventBus) -> None:
        # Lắng nghe event
        event_bus.on("user.created", self.handle_user_created)

    def handle_user_created(self, payload):
        print(f"[Event Received] User Created: {payload}")
```

---

## 4. Sử dụng Command và Query (Use Cases)

App sử dụng pattern CQRS để cô lập logic thực thi (Command) và logic lấy dữ liệu (Query).

**Tạo Command**:

```python
from src.interfaces import ICommand, IEventBus
from dataclasses import dataclass

@dataclass
class CreateUserDto:
    username: str

class CreateUserCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        # Dựa theo type hint, container sẽ tự truyền IEventBus vào
        self.event_bus = event_bus

    def execute(self, dto: CreateUserDto):
        print(f"Creating user {dto.username}...")
        # Phát sự kiện
        self.event_bus.emit("user.created", dto.username)
        return {"status": "success", "user": dto.username}
```

**Thực thi Command qua App**:

```python
from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus

# Khởi tạo App
container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)

# Đăng ký Dependency cốt lõi để các module/command khác có thể truy xuất (như self.event_bus ở trên)
container.singleton(IEventBus, event_bus)

app.boot()

# Execute Use case
result = app.execute(CreateUserCommand, CreateUserDto(username="jules"))
```

---

## 5. Sử dụng EventBus

EventBus được dùng để các module giao tiếp một cách lỏng lẻo. Hệ thống có `MemoryEventBus` (sync), `ThreadPoolEventBus` (background), `AsyncioEventBus` (async).

**Subscribe (Lắng nghe)**:
```python
def on_order_placed(order_id):
    print(f"Sending email for order {order_id}")

event_bus.on("order.placed", on_order_placed)
```

**Emit (Phát tín hiệu)**:
```python
event_bus.emit("order.placed", 123)
```

---

## 6. Sử dụng Middleware

Middleware có thể can thiệp vào quá trình thực thi của mọi Command/Query, hữu dụng cho Validation, Timing, Logging.

**Ví dụ Time Middleware**:

```python
import time
from src.interfaces import IMiddleware, ICommand, IQuery
from typing import Union, Any

class TimingMiddleware(IMiddleware):
    def handle(self, command_or_query: Union[ICommand, IQuery], payload: Any, next_middleware: callable):
        start = time.time()
        result = next_middleware(command_or_query, payload)
        duration = time.time() - start

        name = command_or_query.__class__.__name__
        print(f"[Timing] {name} executed in {duration:.4f}s")
        return result

# Đăng ký vào app
app.use_middleware(TimingMiddleware())
```

---

## 7. Configuration (Cấu hình)

Framework đi kèm `ConfigManager` hỗ trợ lấy dữ liệu từ `dict`, `json file`, hoặc tham số môi trường (`os.environ`).

```python
from src.infra.config_manager import ConfigManager, DictSource, JsonSource, EnvSource
from src.interfaces import IConfig

config = ConfigManager()
config.add_source(DictSource({"app.env": "production"}))
config.add_source(JsonSource("config.json")) # Ghi đè nếu có

# Khai báo cấu hình vào container để Dependency Injection sử dụng được
container.singleton(IConfig, config)

# Truy xuất trong code
env = config.get("app.env", "dev")
```

---

## 8. Sử dụng Logging

Framework có tích hợp sẵn module log cơ bản dựa trên thư viện chuẩn (`StdLogger`). Để sử dụng, bạn chỉ cần đăng ký `LoggerModule`:

```python
from src.modules.logger_module import LoggerModule
from src.interfaces import ILogger

app.use(LoggerModule())

# Khi cần log thông tin trong class
class MyService:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def do_work(self):
        self.logger.info("Service is doing work...")
```

---

## 9. Viết Test với Testing Helpers

Framework có cung cấp các hàm hỗ trợ test tiện lợi trong thư mục `tests/helpers.py`. Các fixture thông dụng cũng có trong `tests/conftest.py`.

Ví dụ viết test bằng `pytest`:

```python
from tests.helpers import assert_event_emitted
from src.app_kernel import App
from my_app.application.commands import CreateUserCommand

def test_create_user_emits_event(app: App, event_bus):
    # Thực thi
    app.execute(CreateUserCommand, "john_doe")

    # Dùng test helper để kiểm tra EventBus
    assert_event_emitted(event_bus, "user.created", times=1)
```

**Thực thi Unit Test**:

```bash
python -m pytest tests/
```
