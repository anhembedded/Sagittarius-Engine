from src.core import App, BaseModule, ICommand, IEventBus

class LoggingModule(BaseModule):
    def boot(self, app: App) -> None:
        def on_booted(data):
            print("[LoggingModule] App has booted successfully.")
        app.event_bus.on('app.booted', on_booted)

class GreetCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    def execute(self, input_dto: dict) -> str:
        name = input_dto.get("name", "Guest")
        message = f"Hello, {name}!"
        self.event_bus.emit('greeted', {"message": message})
        return message

if __name__ == "__main__":
    app = App()
    app.use(LoggingModule())

    def on_greeted(data):
        print(f"[Event Handler] 'greeted' event received. Message: {data['message']}")

    app.event_bus.on('greeted', on_greeted)

    app.boot()

    result = app.execute(GreetCommand, {"name": "World"})
    print(f"Command Result: {result}")
