# TASK-004: Core Engine Safety & Cloud Storage Test Suite

- **Status**: 📝 Planned (Backlog)
- **Priority**: P2 - Medium
- **Category**: Testing & Quality Assurance

---

## 🎯 Goal
Fulfill core engine safety tests and mock coverage for cloud infrastructure adapters (AWS S3, Azure Blob Storage) and circular dependency detection.

---

## 📐 Target Test Groups

### Group 1: Core Engine Safety
- **Circular Dependency Cycle Detection**: Update `StdLibContainer.resolve()` to catch circular type hints and raise `DependencyResolutionError`.
- **Transaction Rollback Middleware**: Implement `TransactionMiddleware(IMiddleware)` for SQLAlchemy sessions.
- **ThreadManager Unit Tests**: Test worker limits, task submission futures, and graceful thread shutdown.

### Group 2: Cloud Storage Mocks
- **S3 & Azure Blob Storage Unit Tests**: Mock `boto3` and `BlobServiceClient` to test read, write, delete, and 404 error handling without hitting live cloud APIs.

---

## 📋 Implementation Checklist
- [ ] Implement circular dependency cycle detection in `std_container.py`.
- [ ] Implement `TransactionMiddleware` in `sagittarius_engine/middleware/`.
- [ ] Write unit tests for `S3FileStorage` and `AzureBlobStorage`.
