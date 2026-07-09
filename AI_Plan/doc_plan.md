# Sagittarius Engine Documentation Roadmap v1

## 🎯 Vision

Documentation không chỉ mô tả API.

Documentation là **specification**, **learning path** và **developer experience** của Sagittarius Engine.

Mục tiêu là đạt chất lượng tương đương:

* Microsoft .NET Documentation
* ASP.NET Core
* Rust Book
* FastAPI
* Kubernetes

---

# Documentation Principles

Mọi tài liệu phải dạy **Concept trước API**.

Learning Path:

```text
Getting Started
        │
        ▼
Core Concepts
        │
        ▼
Runtime
        │
        ▼
Advanced Topics
        │
        ▼
Tutorials
        │
        ▼
API Reference
        │
        ▼
Migration
```

---

# Documentation Rules

Mỗi document phải trả lời được:

```text
What?

Why?

When?

When NOT?

How?

Example

Diagram (nếu cần)

Best Practices

Common Mistakes

Related APIs
```

---

# Documentation Standards

* Chỉ sử dụng Public API

```python
from sagittarius_engine import ...
```

* Không import internal packages.

* Không dùng deprecated APIs.

* Không giải thích implementation.

* Không dùng screenshot.

* Ưu tiên Mermaid.

---

# ✅ Phase D1 — Documentation Foundation

**Status:** Completed

## Goal

Tạo nền tảng cho toàn bộ documentation.

---

## Deliverables

```text
docs/

index.md

STYLE_GUIDE.md

DOC_REVIEW_CHECKLIST.md

getting-started/

    installation.md

    first_app.md

    first_extension.md

    project_templates.md
```

---

## Nội dung

### Landing Page

Giới thiệu:

* Sagittarius Engine là gì?
* Application Engine Philosophy
* Who is this for?
* Who is this NOT for?
* Learning Path
* Mermaid Architecture Diagram

---

### Style Guide

Định nghĩa:

* Documentation as Code
* Terminology
* Mermaid Rules
* Code Example Rules
* Formatting
* Admonitions

---

### Getting Started

Bao gồm:

* Installation
* First App
* First Extension
* SDK Templates

---

## Acceptance

* Landing page hoàn chỉnh
* Getting Started hoàn chỉnh
* Style Guide hoàn chỉnh

---

# 🚧 Phase D1.5 — Documentation Infrastructure

## Goal

Biến docs thành một website.

---

## Deliverables

```text
mkdocs.yml
```

Material Theme

Navigation

Search

Dark Mode

Versioning (Mike)

---

## Acceptance

```bash
mkdocs serve
```

chạy thành công.

---

# 🚧 Phase D1.6 — Documentation Quality

## Goal

Đảm bảo docs luôn đúng.

---

## Deliverables

```text
tests/

    test_docs.py
```

Github Actions

```text
.github/workflows/docs.yml
```

---

## Validation

Kiểm tra:

* Markdown Links
* Build Docs
* Python Snippets
* Deprecated APIs
* Public Imports

---

## Acceptance

```bash
pytest

mkdocs build
```

đều pass.

---

# 🚧 Phase D2 — Core Concepts

## Goal

Giải thích tư duy của Sagittarius.

---

## Deliverables

```text
docs/

concepts/

    engine.md

    runtime.md

    dispatcher.md

    dependency_injection.md

    event_bus.md

    middleware.md

    extensions.md

    lifecycle.md
```

---

## Nội dung

Không giải thích API.

Chỉ giải thích:

* WHY
* DESIGN
* RELATIONSHIPS

Có Mermaid diagrams.

---

## Acceptance

Đọc xong Concepts,

developer hiểu:

> Sagittarius hoạt động như thế nào.

---

# 🚧 Phase D3 — Runtime Guides

## Goal

Giải thích Runtime Infrastructure.

---

## Deliverables

```text
docs/

runtime/

    hosted_services.md

    scheduler.md

    task_manager.md

    async_runtime.md

    cancellation_token.md
```

---

## Nội dung

Bao gồm:

* lifecycle
* startup
* shutdown
* rollback
* threading
* async

Có sequence diagrams.

Có runnable examples.

---

# 🚧 Phase D4 — Advanced Guides

## Goal

Các chủ đề nâng cao.

---

## Deliverables

```text
docs/

advanced/

    extension_dependencies.md

    architecture.md

    performance.md

    best_practices.md

    troubleshooting.md
```

---

## Nội dung

Ví dụ:

* Dependency Graph
* Topological Sorting
* Performance Tips
* Common Pitfalls
* Large Applications

---

# 🚧 Phase D5 — Tutorials

## Goal

Xây dựng ứng dụng thực tế.

---

## Deliverables

```text
docs/

tutorials/

    desktop_app.md

    worker_service.md

    trading_bot.md

    websocket_client.md

    plugin_system.md
```

---

## Nội dung

Tutorial từng bước.

Từ project trống

↓

Ứng dụng chạy được.

Có hình minh họa bằng Mermaid.

---

# 🚧 Phase D6 — API Reference

## Goal

Sinh API Reference tự động.

---

## Deliverables

```text
docs/

api/

    index.md

    kernel.md

    runtime.md

    extensions.md
```

Sử dụng:

* mkdocstrings
* Docstrings
* Auto Generation

---

## Bao gồm

* App
* EngineContext
* Dispatcher
* EventBus
* IExtension
* IHostedService
* Scheduler
* TaskManager
* CancellationToken

---

# 🚧 Phase D7 — Migration Guides

## Goal

Hỗ trợ người dùng nâng cấp.

---

## Deliverables

```text
docs/

migration/

    from_clean_architecture.md

    deprecated_apis.md

    upgrading.md
```

---

## Nội dung

* API Changes
* Migration Examples
* Deprecated APIs
* Compatibility Notes

---

# 🚧 Phase D8 — Documentation Polish & Release

## Goal

Hoàn thiện tài liệu trước khi phát hành v1.0.

---

## Checklist

* Kiểm tra toàn bộ liên kết.
* Chuẩn hóa Mermaid.
* Chạy tất cả code examples.
* Kiểm tra ngữ pháp và thuật ngữ.
* Đồng bộ giữa code, examples và docs.
* Đảm bảo mọi ví dụ chỉ dùng Public API.
* Hoàn thiện navigation và search.

---

# ✅ Định nghĩa Done

Một phase tài liệu chỉ được đánh dấu **Completed** khi đáp ứng đủ:

* Tất cả tài liệu của phase đã hoàn thành.
* Tất cả code examples chạy được.
* `pytest` pass.
* `mkdocs build` pass.
* Không có broken links.
* Không sử dụng deprecated APIs.
* Tất cả sơ đồ Mermaid render đúng.
* Đã review theo `DOC_REVIEW_CHECKLIST.md`.

---
