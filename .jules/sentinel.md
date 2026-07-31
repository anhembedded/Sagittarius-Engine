## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-05-18 - [Path Traversal bypass due to commonpath prefix matching]
**Vulnerability:** Path traversal verification using only `os.path.commonpath([base, full]) == base` is insufficient because it treats a base path like `/tmp/folder` as valid for a full path like `/tmp/folder2` returning `/tmp/folder`, effectively behaving like a prefix match on the final path component if not appended with a trailing slash.
**Learning:** `os.path.commonpath` can erroneously approve sibling directories that share a string prefix if the developer assumes it guarantees directory containment without checking boundary markers.
**Prevention:** Always pair `os.path.commonpath` containment checks with a `startswith` validation against the base directory strictly appended with an `os.sep` (e.g. `os.path.join(base_path, "")`), or handle path component parsing properly.
