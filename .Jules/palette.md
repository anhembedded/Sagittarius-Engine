## 2024-05-19 - Initial Creation
**Learning:** This file tracks critical UX/accessibility learnings.
**Action:** Always document important a11y patterns found.

## 2024-05-20 - Adding Accessibility in PySide6
**Learning:** For Python UI applications utilizing PySide6/Qt, many core widgets lack accessible names and descriptions by default, making them completely opaque to screen readers.
**Action:** Always add `setAccessibleName` and `setAccessibleDescription` to critical UI components like QTableWidget, QListWidget, QProgressBar, and QPushButton to ensure screen reader users have context.
