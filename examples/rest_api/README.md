# REST API Reference Application

This reference application validates server/HTTP integrations.

## Architecture

- **`HttpHostedService`** (`IHostedService`): Runs a standard library Python `HTTPServer` on a background thread.
- **`RequestHandler`**: Decodes requests and calls `app.dispatch()` to execute commands and queries via the Engine dispatcher.
