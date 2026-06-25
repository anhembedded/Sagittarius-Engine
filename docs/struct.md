myApp/
├── domain/                         # 🟡 Domain Layer (Enterprise Business Rules)
│   ├── __init__.py
│   ├── user.py                     # Entity User, Value Objects
│   ├── order.py                    # Entity Order
│   ├── events.py                   # Domain Events (UserCreated, OrderPlaced...)
│   └── services.py                 # Domain Services (logic nghiệp vụ thuần túy)
│
├── application/                    # 🟢 Application Layer (Use Cases / Ports)
│   ├── __init__.py
│   ├── commands/                   # Commands (thay đổi trạng thái)
│   │   ├── __init__.py
│   │   ├── create_user.py          # CreateUserCommand (ICommand)
│   │   └── place_order.py          # PlaceOrderCommand
│   ├── queries/                    # Queries (truy vấn dữ liệu)
│   │   ├── __init__.py
│   │   ├── list_users.py           # ListUsersQuery (IQuery)
│   │   └── get_order.py            # GetOrderQuery
│   └── contracts/                  # Ports (interface cho infrastructure)
│       ├── __init__.py
│       ├── user_repository.py      # IUserRepository (ABC)
│       └── order_repository.py     # IOrderRepository (ABC)
│
├── infrastructure/                 # 🔴 Infrastructure Layer (Adapters)
│   ├── __init__.py
│   ├── repositories/               # Triển khai repository
│   │   ├── __init__.py
│   │   ├── memory_user_repo.py     # InMemoryUserRepository
│   │   └── sqlite_order_repo.py    # SqliteOrderRepository
│   └── external/                   # Tích hợp bên ngoài (API, email...)
│       ├── __init__.py
│       └── email_service.py        # SmtpEmailService
│
├── adapters/                       # 🔵 Presentation Layer (Input/Output)
│   ├── __init__.py
│   ├── cli/                        # Giao diện dòng lệnh
│   │   ├── __init__.py
│   │   └── commands.py             # argparse / click commands
│   ├── web/                        # Giao diện web (Flask/FastAPI)
│   │   ├── __init__.py
│   │   └── routes.py
│   └── batch/                      # Xử lý batch
│       ├── __init__.py
│       └── csv_processor.py
│
├── modules/                        # 📦 Module đóng gói (auto‑discover)
│   ├── __init__.py
│   ├── user_module/                # Module cho tính năng User
│   │   ├── __init__.py             # Class UserModule(IModule)
│   │   └── ... (có thể import từ domain, application, infrastructure)
│   └── order_module/               # Module cho tính năng Order
│       ├── __init__.py             # Class OrderModule(IModule)
│       └── ...
│
├── config.json                     # Cấu hình (nếu dùng file)
├── main.py                         # Composition Root (entry point chính)
└── main_cli.py                     # (tùy chọn) Entry point dành riêng cho CLI