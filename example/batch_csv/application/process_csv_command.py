import os
import csv
from src.interfaces import ICommand, IEventBus

class ProcessCSVCommand(ICommand):
    def __init__(self, event_bus: IEventBus):
        self.event_bus = event_bus

    def execute(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            self.event_bus.emit('csv.error', f"File not found: {filepath}")
            return

        processed_count = 0
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Domain logic or transformation could happen here
                row['score'] = int(row['score']) + 5
                self.event_bus.emit('csv.row_processed', row)
                processed_count += 1

        self.event_bus.emit('csv.completed', processed_count)
