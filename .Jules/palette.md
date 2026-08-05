## 2024-11-20 - PySide6 Accessibility (ARIA Equivalents)
**Learning:** PySide6 desktop apps require similar accessibility treatment to web apps. Instead of `aria-label`, Qt uses `setAccessibleName()`, `setAccessibleDescription()`, and `setToolTip()` to provide hints for screen readers and visual tooltips for users.
**Action:** Always add `setAccessibleName()` and `setToolTip()` to interactive Qt widgets (like QPushButton, QTextEdit, QLabel) to ensure the desktop UI is accessible and provides helpful feedback, analogous to web ARIA labels.
