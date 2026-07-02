---
type: design_doc
tags: [example, template]
language: python
---

# [Title of Your Design Doc]

## Overview
A brief summary of what this document covers. Keep it short – one or two paragraphs.

## Problem Statement
Describe the problem you're solving. Why is this needed?

## Proposed Solution
Explain your approach at a high level. Mention any patterns, technologies, or architectural decisions.

## Core API / Interface
If this is a module, list the main classes, functions, or endpoints. Use backticks for code references like `UserService` or `authenticate()` to help KB Builder link to the code graph.

- `class UserService`: Handles user registration and authentication.
- `def login(email, password) -> Token`: Authenticates a user and returns a JWT.
- `POST /api/auth/login`: Public endpoint for login.

## Dependencies
What other modules or external libraries does this depend on?

- Internal: `common/config`, `common/logging`
- External: `stripe`, `celery`

## How to Use / Examples
Provide code snippets or step-by-step instructions. Wrap code in fenced blocks with language specified.

```python
from auth import UserService
service = UserService()
token = service.login("user@example.com", "password")
```

## Implementation Notes
Any caveats, performance considerations, or edge cases developers should know about.

## Related Documents
Link to other design docs, API specs, or tickets.

- [Authentication Flow](auth-flow.md)
- [API Spec](openapi.yaml)
