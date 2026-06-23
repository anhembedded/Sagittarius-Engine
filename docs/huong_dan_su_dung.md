# Hướng dẫn sử dụng Framework

Framework được xây dựng dựa trên nguyên tắc **Clean Architecture** và **Domain-Driven Design (DDD)**. Hệ thống phân chia rõ ràng các layer: Domain, Application, Infrastructure và Adapter, kết hợp cùng cơ chế **Event-Driven**.

## 1. Khởi tạo một dự án mới

Để khởi tạo dự án, bạn có thể dùng công cụ scaffold có sẵn:

```bash
python -m src.scaffold my_app
```

Cấu trúc dự án sẽ được tự động tạo với file `main.py` và thư mục `modules`.

## 2. Các thành phần chính

### Core Interfaces (Core.py)
- **`ICommand` / `IQuery`**: Định nghĩa logic xử lý Use Case (execute).
- **`IEventBus`**: Kênh phát và nhận sự kiện (emit / on / off).
- **`IContainer`**: Dependency Injection container (bind / singleton / resolve).
- **`IModule`**: Đóng gói các tính năng độc lập, đăng ký vào App qua `register` và `boot`.
- **`IMiddleware`**: Xử lý logic trung gian (VD: Logging) trước khi Command/Query được thực thi.
- **`ILogger`**: Giao diện logging chung.

### App Pipeline
Bất kỳ khi nào một command hay query được thực thi:
1. `app.execute(CommandClass, dto)`
2. Lệnh đi qua Middleware Pipeline (VD: `LoggingMiddleware`).
3. Lệnh được khởi tạo (Dependency Injection qua `IContainer`).
4. `execute(dto)` được gọi.

### Logging
Framework hỗ trợ `StdLogger` có thể đăng ký tự động:
```python
from src.modules.logger_module import LoggerModule
app.use(LoggerModule())
```

### Configuration
Dùng `ConfigManager` lấy cấu hình từ Dict, Env hoặc file Json:
```python
from src.infra.config_manager import ConfigManager, DictSource
config = ConfigManager()
config.add_source(DictSource({"log.level": "DEBUG"}))
container.singleton(IConfig, config)
```

## 3. Testing
Framework cung cấp sẵn các helper trong `tests/helpers.py`:
- `assert_event_emitted(event_bus, event_name, times)`
- Các pytest fixtures: `app`, `container`, `event_bus` (nằm trong `tests/conftest.py`).

## 4. Ví dụ
Tham khảo thư mục `example/` để xem các ứng dụng thực tế.
