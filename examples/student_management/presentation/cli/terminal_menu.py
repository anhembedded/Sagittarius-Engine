# Clean Architecture - Presentation Layer (CLI Hosted Service Adapter)
import sys
from typing import Any, List
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService, CancellationToken
from sagittarius_engine.extensions.health_check_query import HealthCheckQuery, HealthCheckDTO

from examples.student_management.domain.student import Student, StudentException
from examples.student_management.application.dtos.commands import (
    AddStudentCommand,
    UpdateStudentCommand,
    DeleteStudentCommand,
    GenerateReportCommand,
)
from examples.student_management.application.dtos.queries import (
    ListStudentsQuery,
    SearchStudentsQuery,
)
from examples.student_management.application.use_cases.add_student_use_case import AddStudentUseCase
from examples.student_management.application.use_cases.update_student_use_case import UpdateStudentUseCase
from examples.student_management.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from examples.student_management.application.use_cases.list_students_use_case import ListStudentsUseCase
from examples.student_management.application.use_cases.search_students_use_case import SearchStudentsUseCase
from examples.student_management.application.use_cases.generate_report_use_case import GenerateReportUseCase


class TerminalMenu(IHostedService):
    def __init__(self, app: App) -> None:
        self.app = app
        self.token = CancellationToken()
        self.task = None

    def start(self, context: Any) -> None:
        self.app.event_bus.on("report.completed", self._on_report_completed)
        self.app.event_bus.on("health.updated", self._on_health_updated)
        self.task = self.app.context.tasks.spawn(
            self._run_loop, name="TerminalUI", token=self.token
        )

    def stop(self, context: Any) -> None:
        self.app.event_bus.off("report.completed", self._on_report_completed)
        self.app.event_bus.off("health.updated", self._on_health_updated)
        self.token.cancel()

    def wait_for_exit(self) -> None:
        if self.task and self.task.future:
            try:
                self.task.future.result()
            except Exception:
                pass

    def _run_loop(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            self._print_header()
            print("1. List Students")
            print("2. Add Student")
            print("3. Edit Student")
            print("4. Delete Student")
            print("5. Search Student")
            print("6. View Student Details")
            print("7. Generate GPA Report (Async)")
            print("8. Check System Health")
            print("9. Exit")
            print()
            try:
                choice = input("Select: ").strip()
            except EOFError:
                break
            print()

            if choice == "1":
                self._list_students()
            elif choice == "2":
                self._add_student()
            elif choice == "3":
                self._edit_student()
            elif choice == "4":
                self._delete_student()
            elif choice == "5":
                self._search_student()
            elif choice == "6":
                self._view_student_details()
            elif choice == "7":
                self._generate_report()
            elif choice == "8":
                self._check_system_health()
            elif choice == "9":
                print("Goodbye!")
                from PySide6.QtWidgets import QApplication
                from PySide6.QtCore import QMetaObject, Qt
                instance = QApplication.instance()
                if instance:
                    QMetaObject.invokeMethod(instance, "quit", Qt.QueuedConnection)
                break
            else:
                print("❌ Invalid selection. Please choose between 1 and 9.")
            
            try:
                input("\nPress Enter to continue...")
            except EOFError:
                break

    def _print_header(self) -> None:
        print("\n=================================")
        print(" Student Management System")
        print("=================================")

    def _print_student_table(self, students: List[Student]) -> None:
        if not students:
            print("No students found.")
            return

        header = f"{'Student ID':<12} | {'Full Name':<25} | {'Age':<5} | {'Gender':<8} | {'Major':<20} | {'GPA':<5}"
        print(header)
        print("-" * len(header))
        for s in students:
            print(
                f"{s.student_id:<12} | {s.full_name:<25} | {s.age:<5} | {s.gender:<8} | {s.major:<20} | {s.gpa:<5.2f}"
            )

    def _list_students(self) -> None:
        print("--- List Students ---")
        try:
            students = self.app.dispatch(ListStudentsUseCase, ListStudentsQuery())
            self._print_student_table(students)
        except Exception as e:
            print(f"❌ Error listing students: {e}")

    def _add_student(self) -> None:
        print("--- Add Student ---")
        try:
            student_id = input("Student ID (e.g. STD001): ").strip()
            full_name = input("Full Name: ").strip()
            
            age_str = input("Age: ").strip()
            try:
                age = int(age_str)
            except ValueError:
                print("❌ Age must be an integer.")
                return

            gender = input("Gender: ").strip()
            major = input("Major: ").strip()

            gpa_str = input("GPA (0.0 - 4.0): ").strip()
            try:
                gpa = float(gpa_str)
            except ValueError:
                print("❌ GPA must be a number.")
                return

            cmd = AddStudentCommand(
                student_id=student_id,
                full_name=full_name,
                age=age,
                gender=gender,
                major=major,
                gpa=gpa,
            )
            student = self.app.dispatch(AddStudentUseCase, cmd)
            print(f"\n✅ Student '{student.full_name}' added successfully!")
        except StudentException as e:
            print(f"❌ Validation Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _find_student_by_user_input(self) -> Any:
        student_id = input("Enter Student ID to find: ").strip()
        students = self.app.dispatch(
            SearchStudentsUseCase, SearchStudentsQuery(term=student_id)
        )
        for s in students:
            if s.student_id == student_id:
                return s
        return None

    def _edit_student(self) -> None:
        print("--- Edit Student ---")
        try:
            student = self._find_student_by_user_input()
            if student is None:
                print("❌ Student not found.")
                return

            print(f"\nEditing student: {student.full_name} ({student.student_id})")
            print("Leave input blank to keep the current value.")

            new_student_id = input(f"Student ID [{student.student_id}]: ").strip()
            if not new_student_id:
                new_student_id = student.student_id

            new_name = input(f"Full Name [{student.full_name}]: ").strip()
            if not new_name:
                new_name = student.full_name

            age_input = input(f"Age [{student.age}]: ").strip()
            if age_input:
                try:
                    new_age = int(age_input)
                except ValueError:
                    print("❌ Age must be an integer.")
                    return
            else:
                new_age = student.age

            new_gender = input(f"Gender [{student.gender}]: ").strip()
            if not new_gender:
                new_gender = student.gender

            new_major = input(f"Major [{student.major}]: ").strip()
            if not new_major:
                new_major = student.major

            gpa_input = input(f"GPA [{student.gpa:.2f}]: ").strip()
            if gpa_input:
                try:
                    new_gpa = float(gpa_input)
                except ValueError:
                    print("❌ GPA must be a number.")
                    return
            else:
                new_gpa = student.gpa

            cmd = UpdateStudentCommand(
                id=student.id,
                student_id=new_student_id,
                full_name=new_name,
                age=new_age,
                gender=new_gender,
                major=new_major,
                gpa=new_gpa,
            )
            updated = self.app.dispatch(UpdateStudentUseCase, cmd)
            print(f"\n✅ Student '{updated.full_name}' updated successfully!")
        except StudentException as e:
            print(f"❌ Validation Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _delete_student(self) -> None:
        print("--- Delete Student ---")
        try:
            student = self._find_student_by_user_input()
            if student is None:
                print("❌ Student not found.")
                return

            confirm = input(
                f"Are you sure you want to delete {student.full_name} ({student.student_id})? (y/N): "
            ).strip().lower()
            if confirm == "y":
                cmd = DeleteStudentCommand(id=student.id)
                self.app.dispatch(DeleteStudentUseCase, cmd)
                print("✅ Student deleted successfully!")
            else:
                print("Deletion cancelled.")
        except Exception as e:
            print(f"❌ Error deleting student: {e}")

    def _search_student(self) -> None:
        print("--- Search Student ---")
        term = input("Enter search term (Name or Student ID): ").strip()
        if not term:
            print("❌ Search term cannot be empty.")
            return

        try:
            students = self.app.dispatch(
                SearchStudentsUseCase, SearchStudentsQuery(term=term)
            )
            self._print_student_table(students)
        except Exception as e:
            print(f"❌ Error searching: {e}")

    def _view_student_details(self) -> None:
        print("--- View Student Details ---")
        student = self._find_student_by_user_input()
        if student is None:
            print("❌ Student not found.")
            return

        print(f"\nSystem internal UUID: {student.id}")
        print(f"Student ID:         {student.student_id}")
        print(f"Full Name:          {student.full_name}")
        print(f"Age:                {student.age}")
        print(f"Gender:             {student.gender}")
        print(f"Major:              {student.major}")
        print(f"GPA:                {student.gpa:.2f}")

    def _generate_report(self) -> None:
        print("--- Generate GPA Report (Async) ---")
        try:
            msg = self.app.dispatch(GenerateReportUseCase, GenerateReportCommand())
            print(f"⏳ {msg}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _on_report_completed(self, report_content: str) -> None:
        print(f"\n\n🔔 [Notification] Async GPA Report Generation Completed!")
        print(f"📄 {report_content}")
        print("\nSelect: ", end="", flush=True)

    def _check_system_health(self) -> None:
        print("--- Check System Health ---")
        try:
            status = self.app.dispatch(HealthCheckQuery, HealthCheckDTO())
            print(f"Overall Status: {status.get('status', 'unknown').upper()}")
            print("Component States:")
            for comp, state in status.get("components", {}).items():
                print(f" - {comp.capitalize()}: {state}")
        except Exception as e:
            print(f"❌ Health query failed: {e}")

    def _on_health_updated(self, status: dict) -> None:
        print(f"\n🔔 [Scheduler] Periodic Health check: {status.get('status', 'unknown').upper()}")
        print("Select: ", end="", flush=True)
