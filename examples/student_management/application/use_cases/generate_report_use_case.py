import asyncio
from sagittarius_engine.runtime.tasks.task_manager import TaskManager
from sagittarius_engine.interfaces import IEventBus
from examples.student_management.application.contracts.use_case_ports import (
    IGenerateReportUseCase,
)
from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.domain.events import ReportCompletedEvent
from examples.student_management.application.dtos.commands import GenerateReportCommand


class GenerateReportUseCase(IGenerateReportUseCase):
    def __init__(
        self, repo: IStudentRepository, tasks: TaskManager, event_bus: IEventBus
    ) -> None:
        self.repo = repo
        self.tasks = tasks
        self.event_bus = event_bus

    def execute(self, command: GenerateReportCommand = GenerateReportCommand()) -> str:
        task_ref = []

        async def _generate_report_async(token) -> None:
            task = task_ref[0]
            # Simulate heavy report generation with step-by-step progress
            task.update_progress(0, "Starting report generation...")
            await asyncio.sleep(1.0)

            task.update_progress(25, "Gathering student data...")
            await asyncio.sleep(1.0)

            task.update_progress(50, "Calculating GPAs...")
            await asyncio.sleep(1.0)

            task.update_progress(75, "Formatting report...")
            await asyncio.sleep(1.0)

            task.update_progress(100, "Done!")

            students = self.repo.get_all()
            if not students:
                report_content = "Report Summary: No students registered in the database."
            else:
                avg_gpa = sum(s.gpa for s in students) / len(students)
                report_content = f"Report Summary: Total students = {len(students)}, Average GPA = {avg_gpa:.2f}"

            self.event_bus.emit(ReportCompletedEvent(report_content))

        # Spawn async reporting coroutine in background so the dispatch returns immediately
        task = self.tasks.spawn(_generate_report_async, name="GenerateReport")
        task_ref.append(task)
        return "Async GPA report generation started."


# Alias for backward compatibility
GenerateReportCommandHandler = GenerateReportUseCase
