import cmd2
import argparse
from typing import Any

from src.core import App
from example.CLI_smallApp.application.commands import CreateUserCommand, CreateUserDto
from example.CLI_smallApp.application.queries import ListUsersQuery

class UserCLI(cmd2.Cmd):
    def __init__(self, app: App):
        super().__init__()
        self.app = app
        self.prompt = 'App> '

    create_user_parser = cmd2.Cmd2ArgumentParser()
    create_user_parser.add_argument('id', type=str, help='User ID')
    create_user_parser.add_argument('name', type=str, help='User Name')

    @cmd2.with_argparser(create_user_parser)
    def do_create_user(self, args: argparse.Namespace) -> None:
        """Create a new user"""
        dto = CreateUserDto(user_id=args.id, name=args.name)
        self.app.execute(CreateUserCommand, dto)
        self.poutput(f"Sent CreateUserCommand for {args.name}")

    def do_list_users(self, _: Any) -> None:
        """List all users"""
        users = self.app.query(ListUsersQuery)
        if not users:
            self.poutput("No users found.")
        else:
            for user in users:
                self.poutput(repr(user))
