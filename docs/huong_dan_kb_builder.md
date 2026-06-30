# Hướng dẫn sử dụng: Trình tạo Knowledge Base (KB Builder)

Tài liệu này cung cấp hướng dẫn chi tiết về cách sử dụng công cụ **Knowledge Base Builder** (`build_kb.py`) để tự động phân tích mã nguồn và tạo cơ sở dữ liệu vector AI cho dự án Sagittarius.

## 1. Tổng quan

Công cụ KB Builder có nhiệm vụ:
- Phân tích cú pháp (AST) mã nguồn trong thư mục `src/`.
- Trích xuất các lớp (classes), hàm (functions), docstrings, và kiểu dữ liệu (type hints).
- Tạo embeddings văn bản thông qua mô hình cục bộ (`sentence-transformers/all-MiniLM-L6-v2`).
- Lưu trữ siêu dữ liệu (metadata) dưới dạng JSON và chỉ mục vector bằng thư viện **FAISS**.

Các tệp được tạo ra sẽ nằm trong thư mục `docs/kb/` và đã được cấu hình `.gitignore` để không bị đẩy lên Git (tránh làm nặng kho lưu trữ).

## 2. Cài đặt môi trường

Để giữ cho các gói thư viện phụ thuộc của framework lõi không bị ảnh hưởng, chúng ta sẽ sử dụng một môi trường ảo (virtual environment) riêng biệt cho KB Builder.

### Bước 2.1: Tạo môi trường ảo riêng
Mở terminal tại thư mục gốc của dự án và chạy lệnh sau để tạo môi trường ảo (ví dụ đặt tên là `.venv_kb`):

```bash
# Đối với Linux/macOS
python3 -m venv .venv_kb

# Đối với Windows
python -m venv .venv_kb
```

### Bước 2.2: Kích hoạt môi trường ảo

```bash
# Đối với Linux/macOS
source .venv_kb/bin/activate

# Đối với Windows (Command Prompt)
.venv_kb\Scripts\activate.bat

# Đối với Windows (PowerShell)
.venv_kb\Scripts\Activate.ps1
```

### Bước 2.3: Cài đặt các thư viện phụ thuộc
Sau khi đã kích hoạt môi trường ảo, tiến hành cài đặt các gói cần thiết từ tệp `requirements-kb.txt`:

```bash
pip install -r requirements-kb.txt
```

*Lưu ý: Quá trình này sẽ tải xuống `faiss-cpu`, `sentence-transformers` và các thư viện cần thiết để chạy mô hình AI cục bộ.*

## 3. Chạy công cụ tạo Knowledge Base

Khi môi trường đã sẵn sàng, bạn có thể chạy script để tạo cơ sở dữ liệu.

```bash
python tools/kb_builder/build_kb.py
```

### Các tham số tùy chọn:
Công cụ hỗ trợ các tham số dòng lệnh nếu bạn muốn tùy chỉnh thư mục đầu vào/đầu ra:
- `--src`: Chỉ định thư mục mã nguồn cần phân tích (mặc định là `src`).
- `--out`: Chỉ định thư mục lưu trữ kết quả đầu ra (mặc định là `docs/kb`).

Ví dụ chạy với thư mục tùy chỉnh:
```bash
python tools/kb_builder/build_kb.py --src custom_src --out docs/custom_kb
```

## 4. Kết quả đầu ra (Expected Output)

Sau khi script chạy thành công (bao gồm việc tải mô hình nếu chạy lần đầu, tạo embeddings và build FAISS), bạn sẽ thấy 2 tệp xuất hiện trong thư mục `docs/kb/`:

1. `metadata.json`: Chứa dữ liệu có cấu trúc về mã nguồn của bạn (tên hàm, class, chữ ký hàm, docstrings và ID tương ứng). Tệp này có thể đọc được bằng mắt thường.
2. `codebase.index`: Tệp nhị phân của FAISS chứa các vector embeddings. Hệ thống AI/RAG sẽ sử dụng tệp này để tìm kiếm và truy xuất thông tin ngữ nghĩa một cách cực kỳ nhanh chóng.

## 5. Dọn dẹp

Sau khi tạo xong Knowledge Base, bạn có thể thoát khỏi môi trường ảo bằng lệnh:

```bash
deactivate
```
