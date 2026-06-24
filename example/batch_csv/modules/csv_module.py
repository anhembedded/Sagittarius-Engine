from src.base_module import BaseModule
from src.app_kernel import App
from example.batch_csv.application.process_csv_command import ProcessCSVCommand

class CSVModule(BaseModule):
    def register(self, app: App) -> None:
        app.container.bind(ProcessCSVCommand, ProcessCSVCommand)

    def boot(self, app: App) -> None:
        app.event_bus.on('csv.row_processed', lambda data: print(f"Row processed: {data}"))
        app.event_bus.on('csv.completed', lambda count: print(f"Completed processing {count} rows."))
        app.event_bus.on('csv.error', lambda msg: print(f"Error: {msg}"))
