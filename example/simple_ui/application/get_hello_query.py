from src.core import IQuery

class GetHelloQuery(IQuery):
    def execute(self, name: str) -> str:
        return f"Hello, {name or 'World'}!"
