import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.app_kernel import App
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.interfaces import IEventBus

from example.batch_csv.modules.task_module import TaskModule
from example.batch_csv.application.commands import CreateTaskCommand, CreateTaskDto
from example.batch_csv.application.queries import ListTasksQuery

def setup_app():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Core dependencies
    container.singleton(IEventBus, event_bus)

    # Boot app and auto-discover modules
    app.boot(auto_discover="example.batch_csv.modules")
    return app

def generate_csv(filepath: str):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name'])
        writer.writerow(['1', 'Task One'])
        writer.writerow(['2', 'Task Two'])

def main():
    input_file = 'input.csv'
    output_file = 'output.txt'

    # Setup environment
    app = setup_app()
    generate_csv(input_file)

    print(f"Reading from {input_file}...")

    # Process CSV
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_transfer_obj = CreateTaskDto(id=row['id'], name=row['name'])
            app.execute(CreateTaskCommand, data_transfer_obj)

    # Output results
    tasks = app.execute(ListTasksQuery, None)

    with open(output_file, 'w') as f:
        for task in tasks:
            f.write(f"Processed Task: {task.id} - {task.name}\n")

    print(f"Processing complete. Check {output_file}.")

if __name__ == "__main__":
    main()
