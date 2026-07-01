---
type: design_doc
tags: [sagittarius, storage]
language: python
---

# FileStorage

## Overview
The FileStorage component abstracts the operations of reading, writing, and deleting files. By coding against the `IFileStorage` interface, the application can switch between local disk storage and cloud storage providers without changing business logic.

## Problem Statement
Hardcoding file paths and utilizing `open()` directly tightly couples an application to a local file system. This becomes problematic when deploying to cloud environments where local storage is ephemeral, or when horizontal scaling requires a centralized object store like AWS S3 or Azure Blob Storage.

## Proposed Solution
Sagittarius offers `IFileStorage` with three built-in implementations:
- **`LocalFileStorage`**: Writes to the local filesystem. Excellent for development and testing.
- **`S3FileStorage`**: Interacts with Amazon S3. Requires `boto3`.
- **`AzureBlobStorage`**: Interacts with Azure Blob Storage. Requires `azure-storage-blob`.

## Core API / Interface

### `interface IFileStorage` (in `src/interfaces/i_file_storage.py`)
- `def read(self, path: str) -> bytes`: Reads a file.
- `def write(self, path: str, data: Union[bytes, str]) -> None`: Writes data to a file.
- `def delete(self, path: str) -> None`: Deletes a file.
- `def exists(self, path: str) -> bool`: Checks if a file exists.

### Implementations

#### `class LocalFileStorage(IFileStorage)` (in `src/infra/local_file_storage.py`)
- `def __init__(self, base_path: str = "") -> None`: Sets a root directory for operations. Automatically creates parent directories when writing if they do not exist.

#### `class S3FileStorage(IFileStorage)` (in `src/infra/s3_file_storage.py`)
- `def __init__(self, bucket_name: str) -> None`: Requires the AWS bucket name. Instantiates a `boto3.client('s3')`.
- Raises an `ImportError` on instantiation if `boto3` is not installed.

#### `class AzureBlobStorage(IFileStorage)` (in `src/infra/azure_blob_storage.py`)
- `def __init__(self, connection_string: str, container_name: str) -> None`: Connects using the official Azure SDK.
- Raises an `ImportError` on instantiation if `azure-storage-blob` is not installed.

## Dependencies
- Internal: `IFileStorage`
- External: `os`, `shutil`, `boto3` (Optional), `azure-storage-blob` (Optional).

## How to Use / Examples

```python
from src.infra.local_file_storage import LocalFileStorage
from src.infra.s3_file_storage import S3FileStorage

# Setup Local Storage
storage = LocalFileStorage(base_path="/tmp/myapp_uploads")

# Or Setup S3 Storage (if boto3 is installed and configured)
# storage = S3FileStorage(bucket_name="my-app-assets")

# Usage is identical regardless of the underlying infrastructure
filename = "user_avatar_123.png"

if not storage.exists(filename):
    storage.write(filename, b"fake_image_data")

data = storage.read(filename)
storage.delete(filename)
```

## Implementation Notes
- **String vs Bytes**: The `write` method accepts both `str` and `bytes`. If a `str` is passed to the cloud implementations, it is automatically encoded to `utf-8` bytes before upload. The `read` method always returns `bytes`.
- **Optional Dependencies**: The framework itself does not force `boto3` or `azure-storage-blob` in `requirements.txt`. It uses `try/except ImportError` blocks. It is the developer's responsibility to install the required libraries when utilizing these specific classes.

## Related Documents
- `container.md`
