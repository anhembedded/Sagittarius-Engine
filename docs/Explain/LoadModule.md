## 🔍 "Load module" nghĩa là gì?

Trong framework của bạn, một **Module** (implement `IModule`) là **một gói trọn vẹn** gồm domain, application, infrastructure cho một tính năng (ví dụ: User, Order).  

"Load module" là quá trình framework **kích hoạt** module đó, bằng cách gọi hai phương thức của nó:

1. **`register(app)`** – đăng ký các ràng buộc (bindings) vào container, ví dụ:  
   - `bind(ICommand, ConcreteCommand)`  
   - `singleton(IRepository, ConcreteRepository)`

2. **`boot(app)`** – thực hiện các thiết lập khi khởi động, ví dụ:  
   - Đăng ký event handler: `event_bus.on('user.created', handler)`  
   - Kết nối database, kiểm tra cấu hình…

Sau khi load xong, module **sẵn sàng hoạt động**.

---

## 🆚 Module loaded vs Not loaded

| Trạng thái | Chuyện gì xảy ra? |
|------------|-------------------|
| **Đã load** (loaded) | – Các class của module được đưa vào DI Container → app có thể `resolve` và sử dụng.<br>– Event handler của module được gắn vào EventBus → khi có event, handler sẽ chạy.<br>– Module có thể chạy code khởi tạo (boot). |
| **Chưa load** (not loaded) | – File code nằm im trên đĩa, không được đăng ký gì cả.<br>– Container không biết các class đó, nên `resolve` sẽ lỗi.<br>– Event handler không được gắn → event không được xử lý.<br>– **Toàn bộ tính năng của module không hoạt động.** |

> **Nói đơn giản**: Load = bật công tắc. Không load = tắt công tắc.

---

## 📦 Ví dụ cụ thể

Giả sử bạn có hai thư mục module:

```
modules/
├── user_module/    (có class UserModule)
└── order_module/   (có class OrderModule)
```

Trong `main.py`, bạn gọi:
```python
app.boot(auto_discover="modules")
```

Framework sẽ **tự động tìm và load cả hai module**. Sau đó:
- Bạn có thể gọi `app.execute(CreateUserCommand, ...)` và `app.execute(CreateOrderCommand, ...)`.
- Event `user.created` và `order.created` đều được lắng nghe.

Nếu bạn **xóa thư mục `order_module/`** (hoặc không đặt nó trong `modules/`), thì:
- `OrderModule` không được load.
- `CreateOrderCommand` không có trong container → gọi `app.execute(CreateOrderCommand)` sẽ lỗi.
- Event `order.created` sẽ không có ai xử lý.

Đây là cách bạn **bật/tắt tính năng** mà không cần sửa code `main.py`.

---

## ⚙️ Auto‑discovery giúp load tự động

Thay vì load thủ công từng module:
```python
app.use(UserModule())
app.use(OrderModule())
```

Auto‑discovery **quét thư mục `modules/`**, tìm các class `IModule`, rồi tự động gọi `app.use()`. Như vậy bạn chỉ cần thêm thư mục module vào là nó được load, bỏ đi là không load.

Hy vọng đã rõ nghĩa! Bạn còn thắc mắc gì nữa không?