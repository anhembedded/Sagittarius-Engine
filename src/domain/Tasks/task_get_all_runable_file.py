
from Domain.Tasks.task_contextBase import ITaskContext
from Domain.Tasks.TaskBase import AbstractTask
import os

class RunnableFileData:
    def __init__(self):
        self._data: list[dict[str, str]] = []
        
    def add_file(self, name: str, full_path: str):
        self._data.append({"name": name, "fullpath": full_path})
        
    def get_data(self) -> list[dict[str, str]]:
        return self._data
        
    def size(self) -> int:
        return len(self._data)


class Task_Get_All_Runable_File(AbstractTask):
    def __init__(self, path: str = ""):
        self._target_folder = path 

    def run(self, ctx: ITaskContext) -> RunnableFileData:  
        result = RunnableFileData()
        if not self._target_folder or not os.path.exists(self._target_folder):
            return result
        for filename in os.listdir(self._target_folder):
            full_path = os.path.join(self._target_folder, filename)
            if os.path.isfile(full_path):
                result.add_file(filename, os.path.abspath(full_path))
        return result
