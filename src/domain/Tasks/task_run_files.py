from abc import ABC
from abc import abstractmethod
import subprocess
from Domain.Tasks.task_contextBase import ITaskContext
from Domain.Tasks.util.helper import OS_Type, Helper
from Domain.Tasks.TaskBase import AbstractTask

class ITaskRunFiles(ABC):
    @abstractmethod
    def run(self, ctx: ITaskContext):
        pass

class TaskRunFilesWindows(ITaskRunFiles):
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self, ctx: ITaskContext):
        try:
            # subprocess.run với shell=True tương đương os.system nhưng an toàn hơn
            subprocess.run(f"start {self.file_path}", shell=True, check=True)
            ctx.report_message("File opened successfully")
        except Exception as e:
            ctx.report_message(f"Error opening file: {str(e)}")    

class TaskRunFilesLinux(ITaskRunFiles):
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self, ctx: ITaskContext):
        try:
            # Trên Linux thường dùng xdg-open
            subprocess.run(["xdg-open", self.file_path], check=True)
            ctx.report_message("File opened successfully")
        except Exception as e:
            ctx.report_message(f"Error opening file: {str(e)}")    
        

class Factory_Task_Run_Files():
    def create(self, file_path) -> ITaskRunFiles:
        if Helper.get_what_os() == OS_Type.WINDOWS:
            return TaskRunFilesWindows(file_path)
        elif Helper.get_what_os() == OS_Type.LINUX_MAC:
            return TaskRunFilesLinux(file_path)
        else:
            raise ValueError("Unknown OS")