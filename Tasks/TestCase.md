# CONTEXT
You are an expert Senior Python Architect. We are building "Sagittarius_ForkBoy", a general-purpose Python core engine based on Hexagonal Architecture (Ports & Adapters), CQRS, and Dependency Injection. 
Currently, the core framework is solid, but we need to implement critical missing test cases and infrastructure code to ensure it's production-ready for I/O-heavy Trading Bots, IoT embedded systems, and PySide Desktop Apps.

# YOUR MISSION
Implement the following 3 groups of tasks (Critical, Important, Polish). For each task, write the implementation code (if required) and the corresponding Pytest cases. 

---

## GROUP 1: CRITICAL (Core Engine Safety)

### Task 1.1: Circular Dependency Cycle Detection in DI Container
*   **Target File to Update:** `src/infra/container/std_container.py`
*   **Target Test File:** `tests/test_edge_cases.py` (or create `tests/test_container.py`)
*   **Requirement:** Update the `StdLibContainer.resolve()` method to detect circular dependencies (e.g., ClassA requires ClassB, ClassB requires ClassA) using a tracking mechanism (like `threading.local()` or a `resolving` set passed recursively). If a cycle is detected, raise a `DependencyResolutionError` instead of causing a `RecursionError` (Stack Overflow).
*   **Test:** Write a Pytest case that sets up two classes with circular type hints in their `__init__` and asserts that `DependencyResolutionError` is raised.

### Task 1.2: Transaction Rollback (Data Integrity)
*   **Target File to Create:** `src/middleware/transaction_middleware.py`
*   **Target Test File:** `tests/test_middleware.py`
*   **Requirement:** Implement a `TransactionMiddleware(IMiddleware)` that resolves `ISession` from the container. It should wrap the `next_handler()` in a `try...except` block. If execution succeeds, call `session.commit()`. If an exception occurs, call `session.rollback()` and re-raise the exception.
*   **Test:** Mock an `ISession` and a Command that raises an exception. Assert that `session.rollback()` was called and `session.commit()` was NOT called.

### Task 1.3: ThreadManager Test Coverage
*   **Target Test File:** `tests/infra/test_thread_manager.py` (Create this file)
*   **Requirement:** The implementation `src/infra/thread_manager.py` exists but has no tests. Write robust tests for it.
*   **Test Cases:** 
    1. Verify `submit()` correctly executes a background task and returns a `Future` with the correct result.
    2. Verify max_workers limits parallel execution (mock time).
    3. Verify `shutdown(wait=True)` and `shutdown(wait=False)` behave correctly without hanging the test suite.

---

## GROUP 2: IMPORTANT (Infrastructure & Memory)

### Task 2.1: Cloud Storage Mocking (AWS S3 & Azure Blob)
*   **Target Test File:** `tests/infra/storage/test_s3_file_storage.py` and `tests/infra/storage/test_azure_blob_storage.py`
*   **Requirement:** Write tests for `S3FileStorage` and `AzureBlobStorage`. 
*   **Constraints:** Do NOT connect to real cloud providers. Use `unittest.mock` to mock `boto3.client` and `BlobServiceClient`. Test happy paths (read, write, delete, exists) and error paths (e.g., ClientError 404 for S3).

### Task 2.2: Bound Method Unsubscribe in EventBus (Memory Leak Prevention)
*   **Target Test File:** `tests/test_core.py` or `tests/test_memory_event_bus.py`
*   **Requirement:** In UI apps (like PySide), instance methods are frequently used as event handlers. Ensure the EventBus correctly unsubscribes bound methods.
*   **Test:** Create a dummy class with a method `handle_event(self, data)`. Instantiate it, subscribe the bound method (`bus.on('event', obj.handle_event)`), then unsubscribe (`bus.off('event', obj.handle_event)`). Assert that the `_handlers` list for that event is empty to guarantee no dangling references.

---

## GROUP 3: POLISH (Stability & DB Edge Cases)

### Task 3.1: Concurrent Middleware Execution
*   **Target Test File:** `tests/test_middleware.py`
*   **Requirement:** Ensure `MiddlewarePipeline` is thread-safe. 
*   **Test:** Create a `ThreadPoolExecutor` and dispatch 100 concurrent requests through a `MiddlewarePipeline` populated with a dummy middleware that modifies a DTO. Assert that exactly 100 successful responses are returned and no state contamination occurs between requests.

### Task 3.2: Database Integrity Error Wrapping
*   **Target Test File:** `tests/test_base_repository.py`
*   **Requirement:** Test how `BaseRepository.add()` handles a database integrity error (e.g., duplicate primary key).
*   **Test:** Mock `session.add()` to raise `sqlalchemy.exc.IntegrityError` (or a generic Exception representing it). Assert that the repository either cleanly bubbles this up or handles it according to the framework's design.

---

**Execution Instructions:**
Please implement these tasks group by group. Output the clean, fully-typed Python code for the implementations and the test files. Ensure all imports match the existing project structure (e.g., `from src.core import ...`, `from src.interfaces import ...`).