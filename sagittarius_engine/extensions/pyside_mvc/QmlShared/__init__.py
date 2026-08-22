"""
@brief `QmlShared/` is the QML widget kit's physical home (the `.qml`
files + `qmldir` QML import resolution depends on this exact directory
name — see `runtime/qml_host_view.py`'s `_QML_IMPORT_PATH`). It is no
longer a Python package in its own right; every `.py` file that used to
live here moved to `tokens/`/`runtime/` during the EPIC-001C directory
reorg (2026-08-22).

This `__init__.py` exists for exactly one reason: `log_list_model.py`'s
compatibility shim (see that file) needs `QmlShared` to remain an
importable Python package, because the reference consumer has real code
importing `sagittarius_engine.extensions.pyside_mvc.QmlShared.log_list_model`
directly rather than through this extension's top-level re-exports. Do not
add new Python logic here — new Python belongs in `tokens/`/`runtime/`/
`kit/`/`mvc/`/`safety/` per its actual concern.
"""
