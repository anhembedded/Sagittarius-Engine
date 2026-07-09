Mỗi phase đều chạy test được. Đây là cách mà một tech lead thường làm khi migrate framework.

---

# Mục tiêu cuối cùng

Từ

```text
Sagittarius = Clean Architecture Application
```

thành

```text
Sagittarius = Application Engine
```

Engine chỉ cung cấp:

* DI Container
* Event Bus
* Middleware Pipeline
* Module Loader
* Lifecycle
* Logging
* Configuration
* Threading
* Storage
* Database Adapter
* Metrics

Engine **không biết**

* Domain
* UseCase
* Repository
* CQRS
* Entity

Đó là việc của project sử dụng engine.

---

# Phase 1 - Rename architecture [DONE]

Đây là phase dễ nhất.
Không sửa logic.
Chỉ đổi tên.

## application

↓

```text
kernel
```

application/kernel

↓

```text
kernel
```

application/ports

↓

```text
interfaces
```

application/base

↓

```text
base
```

hoặc

```text
common
```

---

## infrastructure

Không đổi.

Nhưng tách rõ.

```text
infrastructure/

    config/

    logging/

    storage/

    persistence/

    metrics/

    ipc/
```

---

## middleware

Giữ nguyên.

---

## adapters

Giữ nguyên.

---

## modules

Đổi thành

```text
extensions
```

vì đây không phải business module.

---

Sau phase này

project sẽ thành

```text
sagittarius_engine/

    kernel/

    interfaces/

    container/

    event_bus/

    middleware/

    logging/

    config/

    storage/

    persistence/

    adapters/

    extensions/

    tools/
```

---

# Phase 2 - Tách Kernel [DONE]

Hiện tại

App

đang làm quá nhiều việc.

Ví dụ

```python
App
boot()
execute()
query()
use()
middleware
container
event_bus
```

AI sẽ tách thành

```text
kernel/
    app.py
    lifecycle.py
    bootstrap.py
    module_loader.py
    dispatcher.py
```

App chỉ còn

```python
class App:
    start()
    stop()

```

---

# Phase 2.5 - Engine Service Registry & EngineContext [DONE]

Engine Service Registry

Lý do là hiện tại App vẫn giữ trực tiếp các thành phần như:

Container
EventBus
Middleware
Logger
Config

Trong một engine đúng nghĩa, App chỉ nên giữ EngineContext hoặc EngineServices, ví dụ:

app.services.container
app.services.event_bus
app.services.logger
app.services.config

hoặc

engine.container
engine.events
engine.logger

Sau đó mới đến Phase 3 là tách CQRS, Repository, BaseModule... ra thành extensions.

Theo mình, thêm bước này sẽ giúp Sagittarius chuyển hẳn sang tư duy Application Engine thay vì chỉ đổi tên thư mục.


# Phase 3 - Loại bỏ Clean Architecture khỏi engine [DONE]

Đây là phase quan trọng nhất.

Engine KHÔNG nên có

```text
application/

domain/

repository/

```

---

Bỏ khỏi engine

```text
BaseRepository
ICommand
IQuery
BaseModule

```

---

Thay bằng abstraction nhỏ hơn.

Ví dụ

```python
IHandler
IExecutable
ILifecycle

```

hoặc

```python
IService
```

---

CQRS sẽ thành extension.

Ví dụ

```text
extensions/
    cqrs/
        command_bus.py
        query_bus.py

```

---

# Phase 4 - Module System [DONE]

Module hiện tại

đang là

```python
register()

boot()

```

AI sẽ refactor thành

```python
initialize()

start()

stop()

dispose()

```

Lifecycle đầy đủ hơn.

---

# Phase 5 - Extension System

Ví dụ

```text
extensions/
    sqlalchemy/
    health/
    metrics/
    scheduler/
    cqrs/
    pydantic/

```

Không còn nằm trong kernel.
Kernel cực nhỏ.

---

# Phase 6 - Project Layout

Đây mới là điểm mình thích nhất.

Ví dụ user tạo project

```text
TradingBot/
    sagittarius_engine/
    app/

```

Trong app

muốn architecture gì cũng được.

Ví dụ

```text
app/
    domain/
    application/
    infrastructure/

```

hoặc

```text
app/

    services/
    controllers/

```

hoặc

```text
app/
    mvc/

```

Engine không quan tâm.

---

# Phase 7 - API mới

Hiện tại

```python
app.execute(CreateUserCommand())
```

mang hơi hướng CQRS.

Mình sẽ chuyển thành

```python
engine.dispatch(...)
```

hoặc

```python
engine.run(...)
```

CQRS chỉ là extension.

---

# Phase 8 - Đổi package name

Từ

```text
src/
```

↓

```text
sagittarius_engine/
```

Khi tạo project

```text
MyBot/
    sagittarius_engine/
    app/
```

Import

```python
from sagittarius_engine.kernel import App
```

rất tự nhiên.

---

# Phase 9 - Documentation

Đổi hoàn toàn cách giới thiệu.

Không còn

> A Clean Architecture framework

Mà là

> A lightweight Python Application Engine.

---

Giới thiệu chỉ còn

```text
Core

• Dependency Injection
• Event Bus
• Middleware
• Module System
• Configuration
• Logging
• Lifecycle

Extensions

• SQLAlchemy
• Pydantic
• Metrics
• Scheduler
• CQRS
```

Không nhắc tới Domain.
Không nhắc Repository.
Không nhắc Entity.

---
