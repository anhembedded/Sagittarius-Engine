---
type: design_doc
tags: [sagittarius, metrics]
language: python
---

# Metrics

## Overview
The Metrics component provides a standard way to instrument the application. It allows developers to record quantitative data about the system's behavior, such as error rates, request durations, and queue sizes.

## Problem Statement
In production environments, simply logging text is not enough to monitor application health or trigger alerts. Developers need structured metrics (Counters, Timers, Gauges) that can be aggregated and visualized by tools like Prometheus, DataDog, or Grafana. Hardcoding SDKs for these tools directly into business logic breaks Clean Architecture boundaries.

## Proposed Solution
Sagittarius defines the `IMetrics` interface with methods for common metric types. The built-in `LogMetrics` implementation acts as a bridge, formatting these metrics as structured text and pushing them through the existing `ILogger`. This allows for simple metric collection in environments where stdout is ingested by log-parsing agents (like fluentd or ELK).

## Core API / Interface

### `interface IMetrics` (in `src/interfaces/i_metrics.py`)
- `def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None) -> None`: Increments a counter metric.
- `def record_timing(self, name: str, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None`: Records a duration.
- `def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None`: Sets a gauge metric to an absolute value.

### `class LogMetrics(IMetrics)` (in `src/infra/log_metrics.py`)
- `def __init__(self, logger: ILogger) -> None`: Takes an `ILogger` instance to which it will output the metric strings.

## Dependencies
- Internal: `ILogger`
- External: `json`

## How to Use / Examples

```python
from src.interfaces import ILogger
from sagittarius_engine.infrastructure.log_metrics import LogMetrics

def execute_command(metrics: LogMetrics):
    # 1. Increment a counter
    metrics.increment_counter("command.executed",
                              tags={"command_type": "CreateUser"})

    # 2. Record a timing
    metrics.record_timing("db.query.duration", 45.2,
                          tags={"table": "users"})

    # 3. Set a gauge
    metrics.set_gauge("active_users", 1045)

# Example output via logger:
# [METRIC] type=counter name=command.executed value=1 {"command_type": "CreateUser"}
# [METRIC] type=timing name=db.query.duration duration_ms=45.2 {"table": "users"}
# [METRIC] type=gauge name=active_users value=1045
```

## Implementation Notes
- **Tag Serialization**: `LogMetrics` utilizes `json.dumps()` to serialize the dictionary of tags into a string appended to the log message. This makes it easily parseable by JSON log parsers.
- **Extensibility**: Because of the `IMetrics` interface, a user could easily write a `PrometheusMetrics` or `DatadogMetrics` implementation and bind it in the container, completely replacing `LogMetrics` without changing any domain code.

## Related Documents
- `logging.md`
