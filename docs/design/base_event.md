---
type: design_doc
tags: [sagittarius, event]
language: python
---

# BaseEvent

## Overview
`BaseEvent` is a standard utility class designed to represent domain events within the Sagittarius Framework. It standardizes common metadata required for tracing and logging event-driven behaviors.

## Problem Statement
When publishing events to an `IEventBus`, it's best practice to pass structured data objects rather than primitive dictionaries. These objects need unique identifiers for idempotency checks and timestamps for chronological ordering. Duplicating this boilerplate across every event class is tedious and error-prone.

## Proposed Solution
The `BaseEvent` class automatically generates a unique UUID and a timezone-aware UTC timestamp upon instantiation. Domain events can subclass it to inherit this metadata seamlessly. It also provides a helper method to serialize the event into a dictionary, which is useful when logging or transmitting events over networks.

## Core API / Interface

### `class BaseEvent` (in `src/base_event.py`)
- `def __init__(self) -> None`: Initializes `event_id` (UUID4 string) and `occurred_on` (UTC datetime).
- `def to_dict(self) -> dict`: Returns a dictionary representation of the event, with the datetime object correctly serialized to an ISO format string.

## Dependencies
- Internal: None
- External: Standard libraries (`uuid`, `datetime`)

## How to Use / Examples

```python
from src.base_event import BaseEvent

class UserCreatedEvent(BaseEvent):
    """Event emitted when a new user is created."""
    def __init__(self, username: str, email: str):
        super().__init__()  # Crucial: calls BaseEvent.__init__ to generate ID and timestamp
        self.username = username
        self.email = email

# Example Usage
event = UserCreatedEvent(username="alice_wonder", email="alice@example.com")

print(f"Event ID: {event.event_id}")
print(f"Occurred on: {event.occurred_on}")

# Serialize for JSON transport or logging
data = event.to_dict()
# {
#   'event_id': '550e8400-e29b-41d4-a716-446655440000',
#   'occurred_on': '2023-10-15T12:00:00+00:00',
#   'username': 'alice_wonder',
#   'email': 'alice@example.com'
# }
```

## Implementation Notes
- **UTC Time**: The timestamp strictly utilizes `datetime.now(timezone.utc)` (instead of the deprecated `datetime.utcnow()`) to ensure timezone safety.
- **Inheritance is Optional**: `IEventBus` does not explicitly require data payloads to inherit from `BaseEvent`. It is provided purely as an optional utility.

## Related Documents
- `event_bus.md`
