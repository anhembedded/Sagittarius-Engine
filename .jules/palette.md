## 2024-05-18 - Added PySide6 Accessibility (Qt Accessible Names and Descriptions)
**Learning:** PySide6/Qt doesn't use HTML ARIA labels but instead uses its own accessible interfaces. Adding `setAccessibleName()` and `setAccessibleDescription()` directly to UI widgets like `QTableWidget` and `QProgressBar` significantly improves desktop screen reader support without breaking native UI patterns.
**Action:** Always add `setAccessibleName` and `setAccessibleDescription` to informative UI components in desktop applications (PySide/PyQt).
