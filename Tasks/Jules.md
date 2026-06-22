We need to design `main.py` to act as the **Composition Root** 🧩. Its sole job is to read the environment mode (`debug` or `release`), initialize the correct infrastructure resources, wire them into the adapters, and launch the application.

Here is how the wiring flow looks inside the entry point:

| Step | Action | Layer Involved |
| --- | --- | --- |
| 1️⃣ **Parse** | Check if the mode is `debug` or `release`. | System / CLI |
| 2️⃣ **Infra** | Init `tech_logger_infra` (or a silent no-op logger if release). | Infrastructure 🏗️ |
| 3️⃣ **Adapters** | Create exchange or event bus clients using that logger. | Adapters 🔌 |
| 4️⃣ **Use Cases** | Inject adapters into your `print_price_use_case`. | Use Cases ⚙️ |
| 5️⃣ **Run** | Start the main asynchronous loop. | Application Lifecycle |

To handle the logging requirement cleanly without breaking our architecture rules, `main.py` will conditionally instantiate either a real active logger or a silent "dummy" logger based on the startup flag. This keeps the rest of your app completely unaware of whether logging is actually turned on or off.

Before we look at how to write this wiring code, how would you prefer to pass the debug/release flag into your application terminal command?

1. ⌨️ **Command-line arguments:** `python main.py --mode debug`
2. 🌱 **Environment variables:** `MODE=debug python main.py`