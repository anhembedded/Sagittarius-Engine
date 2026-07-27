import asyncio
from sagittarius_engine.runtime.tasks.task_manager import TaskManager
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.application.contracts.use_case_ports import (
    IGenerateReportUseCase,
)
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.application.dtos.commands import GenerateReportCommand


class GenerateReportUseCase(IGenerateReportUseCase):
    def __init__(
        self, repo: IStudentRepository, tasks: TaskManager, event_bus: IEventBus
    ) -> None:
        self.repo = repo
        self.tasks = tasks
        self.event_bus = event_bus

    def execute(self, command: GenerateReportCommand = GenerateReportCommand()) -> str:
        # Spawn async reporting coroutine in background so the dispatch returns immediately
        self.tasks.spawn(self._generate_report_async, name="GenerateReport")
        return "Async GPA report generation started."

    async def _generate_report_async(self, token) -> None:
        # Simulate heavy report generation with step-by-step progress
        self.event_bus.emit("report.progress", 0)
        await asyncio.sleep(1.0)

        self.event_bus.emit("report.progress", 25)
        await asyncio.sleep(1.0)

        self.event_bus.emit("report.progress", 50)
        await asyncio.sleep(1.0)

        self.event_bus.emit("report.progress", 75)
        await asyncio.sleep(1.0)

        self.event_bus.emit("report.progress", 100)

        students = self.repo.get_all()
        if not students:
            report_content = "Report Summary: No students registered in the database."
        else:
            avg_gpa = sum(s.gpa for s in students) / len(students)
            report_content = f"Report Summary: Total students = {len(students)}, Average GPA = {avg_gpa:.2f}"

        self.event_bus.emit("report.completed", report_content)


# Alias for backward compatibility
GenerateReportCommandHandler = GenerateReportUseCase
