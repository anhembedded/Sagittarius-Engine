import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.app_kernel import App
from src.interfaces import IEventBus
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.modules.logger_module import LoggerModule
from example.batch_csv.modules.csv_module import CSVModule
from example.batch_csv.application.process_csv_command import ProcessCSVCommand

def generate_sample_csv(filepath):
    import csv
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'score'])
        writer.writerow(['1', 'Alice', '85'])
        writer.writerow(['2', 'Bob', '90'])
        writer.writerow(['3', 'Charlie', '78'])

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IEventBus, event_bus)

    app.use(LoggerModule())
    app.use(CSVModule())
    app.boot()

    generate_sample_csv('sample.csv')
    app.execute(ProcessCSVCommand, 'sample.csv')

if __name__ == "__main__":
    main()
