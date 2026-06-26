## 🧩 Từng bước tạo **một Module** – Hiểu rõ tại sao và như thế nào

Mình sẽ lấy ví dụ cụ thể: **Module quản lý Task**. Mục tiêu: thêm tính năng tạo Task và liệt kê Task vào app.  
Mọi thứ được giải thích **chi tiết**, gắn với nguyên tắc Clean Architecture và cách framework vận hành.

### 🔷 1. Module là gì trong framework này?
- Mỗi Module là một **gói trọn vẹn** cho một tính năng (User, Task, Order…).
- Nó gồm đầy đủ các tầng: Domain → Application (Port + UseCase) → Infrastructure (Adapter) → (Adapter giao tiếp thì để riêng).
- Module sẽ **tự đăng ký** (bind) các class cần thiết vào DI container và **tự đăng ký** event handler khi app boot.
- Nhờ vậy, bạn có thể **thêm một module mới vào app** chỉ bằng cách bỏ thư mục của nó vào `modules/` – không cần sửa `main.py`.

### 🔷 2. Các thành phần của Module (theo thứ tự phụ thuộc từ trong ra ngoài)

```
modules/task_module/
├── __init__.py               # Class TaskModule(IModule) – đầu não của module
└── (không có file khác – mọi thứ được import từ các thư mục tầng ngoài: domain, application, infrastructure)
```
> Thực tế, bạn để code Domain, Application, Infrastructure ở thư mục riêng (domain/, application/, infrastructure/) trong project. Module chỉ là nơi **kết nối** chúng.

---

## 🔶 Bắt đầu làm Module

Giả sử project của bạn có cấu trúc như sau:

```
myTaskApp/
├── domain/
├── application/
│   ├── contracts/
│   ├── commands/
│   └── queries/
├── infrastructure/
│   └── repositories/
├── modules/
└── main.py
```

Bạn sẽ lần lượt tạo từng tệp.

---

### ✅ Bước 1 – Domain: Định nghĩa Entity và Domain Event

**Tệp:** `domain/task.py`

```python
class Task:
    def __init__(self, task_id: int, title: str):
        self.id = task_id
        self.title = title
```

**Tệp:** `domain/events.py`

```python
class TaskCreated:
    def __init__(self, task):
        self.task = task
```

> **Tại sao?**  
> – Entity là đối tượng nghiệp vụ thuần túy, không phụ thuộc gì.  
> – Domain Event là sự kiện xảy ra trong domain, để các thành phần khác phản ứng.

---

### ✅ Bước 2 – Application Port: Khai báo interface cho Repository

**Tệp:** `application/contracts/task_repository.py`

```python
from abc import ABC, abstractmethod
from myTaskApp.domain.task import Task

class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task) -> None: ...
    @abstractmethod
    def all(self) -> list[Task]: ...
```

> **Tại sao?**  
> – Đây là **port** (cổng) theo Clean Architecture. Use Case chỉ phụ thuộc vào interface này, không biết implementation cụ thể.  
> – Đảm bảo **dependency inversion**: Infrastructure sẽ phụ thuộc vào Application (implement interface này).

---

### ✅ Bước 3 – Application Use Cases: Viết Command và Query

**Command:** `application/commands/create_task.py`

```python
from src.core import ICommand, IEventBus
from myTaskApp.application.contracts.task_repository import ITaskRepository
from myTaskApp.domain.task import Task
from myTaskApp.domain.events import TaskCreated

class CreateTaskCommand(ICommand):
    def __init__(self, repo: ITaskRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, data_transfer_obj: dict):
        task = Task(task_id=data_transfer_obj['id'], title=data_transfer_obj['title'])
        self.repo.add(task)
        self.event_bus.emit('task.created', TaskCreated(task))
        return task
```

> **Tại sao?**  
> – Command đại diện cho một use case làm thay đổi trạng thái.  
> – Nó nhận `ITaskRepository` (interface) và `IEventBus` qua constructor – framework DI sẽ tự inject.  
> – Sau khi tạo task, nó emit event để các module khác (hoặc chính module này) có thể xử lý (ví dụ ghi log, gửi mail).

**Query:** `application/queries/list_tasks.py`

```python
from src.core import IQuery
from myTaskApp.application.contracts.task_repository import ITaskRepository

class ListTasksQuery(IQuery):
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def execute(self, _=None) -> list:
        return self.repo.all()
```

> **Tại sao?**  
> – Query không thay đổi trạng thái, chỉ đọc dữ liệu.  
> – Cũng dùng port `ITaskRepository` để không phụ thuộc vào chi tiết lưu trữ.

---

### ✅ Bước 4 – Infrastructure: Triển khai Repository thực sự

**Tệp:** `infrastructure/repositories/memory_task_repo.py`

```python
from myTaskApp.application.contracts.task_repository import ITaskRepository
from myTaskApp.domain.task import Task

class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._tasks = []

    def add(self, task: Task):
        self._tasks.append(task)

    def all(self) -> list[Task]:
        return self._tasks
```

> **Tại sao?**  
> – Đây là **adapter** cho port. Có thể thay bằng `SqliteTaskRepository` sau mà không cần sửa use case.

---

### ✅ Bước 5 – Module: Kết nối tất cả lại

**Tệp:** `modules/task_module/__init__.py`

```python
from src.core import BaseModule, App
from myTaskApp.application.contracts.task_repository import ITaskRepository
from myTaskApp.infrastructure.repositories.memory_task_repo import InMemoryTaskRepository
from myTaskApp.application.commands.create_task import CreateTaskCommand
from myTaskApp.application.queries.list_tasks import ListTasksQuery

class TaskModule(BaseModule):
    def register(self, app: App):
        # Đăng ký repository như một singleton (dùng chung cho cả app)
        app.container.singleton(ITaskRepository, InMemoryTaskRepository())

        # Đăng ký command & query – mỗi lần gọi sẽ tạo instance mới
        app.container.bind(CreateTaskCommand, CreateTaskCommand)
        app.container.bind(ListTasksQuery, ListTasksQuery)

    def boot(self, app: App):
        # Lắng nghe sự kiện task.created để in thông báo
        app.event_bus.on('task.created', self.when_task_created)

    def when_task_created(self, event):
        print(f"[TaskModule] New task created: {event.task.title}")
```

> **Tại sao?**  
> – `register()`: nơi khai báo **cách tạo** các object.  
>   - Repository là singleton để toàn app dùng chung một kho dữ liệu.  
>   - Command/Query không cần singleton, mỗi lần `app.execute` sẽ resolve ra instance mới.  
> – `boot()`: nơi đăng ký **event handler**. Khi app boot, handler này sẽ được gắn vào EventBus.  
> – Module kế thừa `BaseModule`, auto‑discovery sẽ tự tìm và gọi `app.use(task_module_instance)`.

---

### ✅ Bước 6 – main.py: Khởi động app (Composition Root)

**Tệp:** `main.py`

```python
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.core import App, IContainer, IEventBus

container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)

# Đăng ký các service cốt lõi
container.singleton(IContainer, container)
container.singleton(IEventBus, event_bus)

# Tự động quét và load tất cả module trong thư mục modules/
app.boot(auto_discover="modules")

# Bây giờ có thể gọi app.execute(...) từ CLI hoặc bất kỳ adapter nào
```

> **Tại sao?**  
> – Composition Root là nơi duy nhất biết đến các implementation cụ thể (StdLibContainer, MemoryEventBus).  
> – Việc auto‑discover giúp bạn không cần liệt kê từng module.

---

## 🎯 Tổng kết: Khi muốn thêm tính năng mới, bạn chỉ cần

1. Tạo Entity / Domain Event (domain/)
2. Tạo interface Port (application/contracts/)
3. Viết Use Case (Command/Query)
4. Viết implementation cho Port (infrastructure/)
5. Tạo **một file module** (modules/xxx/__init__.py) để nối chúng lại
6. Bỏ vào thư mục modules – app tự load

> **Không cần sửa main.py, không cần sửa code cũ.**  
> Module mới hoàn toàn độc lập, tuân thủ Open/Closed Principle.

Bạn có thể kiểm tra: chỉ cần xóa thư mục `modules/task_module/` đi, app vẫn chạy bình thường (chỉ mất tính năng Task). Đó là sức mạnh của kiến trúc module hóa và auto‑discovery.