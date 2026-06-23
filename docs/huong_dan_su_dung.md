# Hướng Dẫn Sử Dụng Application Framework

Tài liệu này cung cấp các hướng dẫn chi tiết và các Use Case phổ biến khi sử dụng Application Framework (Clean Architecture) của hệ thống. Tất cả được viết hoàn toàn bằng Python Standard Library.

---

## 1. Bắt Đầu Nhanh (Quick Start)

**Mục đích:** Khởi tạo một dự án mới cực kỳ nhanh chóng bằng công cụ Scaffold có sẵn.

**Các bước thực hiện:**
1. Mở terminal và chạy lệnh scaffold:
   ```bash
   python src/scaffold.py MyAwesomeApp
   ```
2. Cấu trúc thư mục mới `MyAwesomeApp` sẽ được tạo ra cùng với `main.py`, `config.json` và thư mục `modules`.
3. Thiết lập biến môi trường `PYTHONPATH` để framework có thể import đúng các module (nếu chạy trực tiếp):
   ```bash
   export PYTHONPATH=$(pwd)
   ```
4. Chạy ứng dụng vừa tạo:
   ```bash
   python MyAwesomeApp/main.py
   ```
   *Kết quả:* Sẽ in ra `Application booted successfully.`

---

## 2. Ứng Dụng Batch (Xử lý hàng loạt)

**Mục đích:** Xử lý dữ liệu từ file (VD: CSV, JSON), chạy qua Use Case và lưu kết quả. Kiến trúc Clean Architecture giúp tách biệt logic đọc/ghi file khỏi Use Case.

**Code Mẫu:**

*Application Layer (Use Case):*
```python
from src.core import ICommand

class ProcessDataCommand(ICommand):
    def execute(self, input_dto: dict):
        # Logic xử lý nghiệp vụ
        return {
            "record_id": input_dto["id"],
            "status": "PROCESSED",
            "value": input_dto["value"] * 2
        }
```

*Adapter Layer (Batch Job):*
```python
import json
from src.core import App

def run_batch_job(app: App, input_file: str, output_file: str):
    results = []
    # 1. Đọc dữ liệu
    with open(input_file, 'r') as f:
        data = json.load(f)

    # 2. Xử lý qua Use Case
    for record in data:
        dto = {"id": record["id"], "value": record["value"]}
        result = app.execute(ProcessDataCommand, dto)
        results.append(result)

    # 3. Ghi kết quả
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    print("Batch processing completed!")
```

---

## 3. Ứng Dụng UI / Web API (FastAPI / Flask / Tkinter)

**Mục đích:** Chứng minh Framework hoàn toàn độc lập với UI. Bạn có thể gắn bất kỳ Web Framework hay Desktop GUI nào như một "Input Adapter".

**Mô tả kiến trúc:**
- Khởi tạo `App` ở bước khởi động của Web Framework.
- Trong các route/controller, đóng gói request thành `DTO` và gọi `app.execute()` hoặc `app.query()`.
- Trả về kết quả HTTP.

**Code Mẫu (với FastAPI - giả định bạn có cài fastapi):**
```python
# adapter_api.py
from fastapi import FastAPI
from src.core import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus

# Command giả định
from application.commands import CreateUserCommand

app_api = FastAPI()

# Composition Root
container = StdLibContainer()
event_bus = MemoryEventBus()
core_app = App(container, event_bus)
core_app.boot(auto_discover="modules")

@app_api.post("/users/")
def create_user(user_id: str, name: str):
    dto = {"id": user_id, "name": name}
    # Web Framework chỉ gọi vào Core App
    result = core_app.execute(CreateUserCommand, dto)
    return {"message": "Success", "user_id": result.id}
```

---

## 4. Xử Lý Domain Event Phức Tạp

**Mục đích:** Ứng phó với các Event có nhiều Handler, hoặc cần lưu lại lịch sử Event (Event Sourcing đơn giản).

**Code Mẫu:**

```python
from src.core import App

# Handler 1: Gửi Email
def send_welcome_email(user):
    print(f"[EmailService] Sending welcome email to {user.name}")

# Handler 2: Cập nhật Analytics
def update_analytics(user):
    print(f"[AnalyticsService] Incrementing user count for user {user.id}")

# Handler 3: Event Store (Lưu trữ lịch sử)
class EventStore:
    def __init__(self):
        self.history = []

    def log_event(self, event_name, data):
        self.history.append({"event": event_name, "data": data})
        print(f"[EventStore] Logged {event_name}")

def register_complex_events(app: App, store: EventStore):
    # Đăng ký nhiều handler cho cùng 1 event
    app.event_bus.on('user.created', send_welcome_email)
    app.event_bus.on('user.created', update_analytics)

    # Bắt tất cả event để lưu vào Store (Cần custom Event Bus để hỗ trợ wildcard,
    # hoặc gắn thủ công vào các event quan trọng)
    app.event_bus.on('user.created', lambda data: store.log_event('user.created', data))
```

---

## 5. Tùy Chỉnh Middleware Pipeline

**Mục đích:** Thay đổi luồng thực thi chung (Logging, Validation, Transaction, Authentication) trước khi tới Use Case.

**Code Mẫu:**

```python
from typing import Any, Callable
from src.core import IMiddleware, App

class AuthMiddleware(IMiddleware):
    def process(self, cmd_or_query: Any, dto: Any, next_handler: Callable[[], Any]) -> Any:
        # Ví dụ: Kiểm tra Authorization
        if dto and dto.get("role") != "ADMIN":
            raise PermissionError("Access Denied! Admin only.")

        print("[AuthMiddleware] User is Admin. Proceeding...")
        return next_handler()

# Cách đăng ký
app.use_middleware(AuthMiddleware())

# Middleware sẽ chạy theo thứ tự được add (chain of responsibility)
# Ví dụ: app.use_middleware(LogMiddleware())
```

*Mẹo:* Nếu muốn áp dụng middleware cho một số Command cụ thể, trong `process`, bạn có thể kiểm tra:
`if cmd_or_query.__class__.__name__ == "CreateUserCommand": ...`

---

## 6. Testing (Kiểm Thử Use Case)

**Mục đích:** Viết Unit Test cho Application Layer cực kỳ dễ dàng nhờ Dependency Injection. Bỏ qua DB thật, ta sẽ dùng Mock.

**Code Mẫu (với pytest):**
```python
import pytest
from unittest.mock import Mock
from application.commands import CreateUserCommand

def test_create_user_command():
    # 1. Arrange: Mock các dependency (Ports)
    mock_repo = Mock()
    mock_event_bus = Mock()

    command = CreateUserCommand(repo=mock_repo, event_bus=mock_event_bus)
    dto = {"id": "123", "name": "John Doe"}

    # 2. Act
    result = command.execute(dto)

    # 3. Assert
    assert result.id == "123"
    assert result.name == "John Doe"

    # Kiểm tra repository.save có được gọi không
    mock_repo.save.assert_called_once()

    # Kiểm tra event có được emit không
    mock_event_bus.emit.assert_called_once_with('user.created', result)
```

---

## 7. Quản Lý Cấu Hình (Configuration System)

**Mục đích:** Đọc cấu hình ưu tiên từ nhiều nguồn khác nhau (Biến môi trường ưu tiên hơn JSON, JSON ưu tiên hơn Default Dict).

**Code Mẫu:**

```python
import os
from src.infra.config_manager import ConfigManager, DictSource, JsonSource, EnvSource

def setup_config():
    config = ConfigManager()

    # 1. Nguồn thấp nhất: Cấu hình mặc định
    config.add_source(DictSource({
        "app_name": "MyApp",
        "debug": False,
        "db_host": "localhost"
    }))

    # 2. Nguồn ưu tiên hơn: File JSON
    config.add_source(JsonSource("config.json"))

    # 3. Nguồn ưu tiên cao nhất: Biến môi trường (prefix 'MYAPP_')
    # Ví dụ: export MYAPP_DB_HOST="remote-server"
    os.environ["MYAPP_DB_HOST"] = "remote-server"
    config.add_source(EnvSource(prefix="MYAPP_"))

    return config

# Sử dụng:
conf = setup_config()
print(conf.get("app_name")) # Lấy từ dict hoặc JSON
print(conf.get("DB_HOST"))  # Lấy từ ENV -> Output: remote-server
```

---
*Tài liệu này bao quát các kịch bản thực tế phổ biến nhất khi áp dụng Framework. Chúc bạn code vui vẻ!*
