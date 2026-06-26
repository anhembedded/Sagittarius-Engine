import sys
import argparse
from src.app_kernel import App
from example.CLI_smallApp.application.commands import CreateUserCommand
from example.CLI_smallApp.application.queries import ListUsersQuery

def run_cli(app: App):
    parser = argparse.ArgumentParser(description="CLI Small App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create-user command
    parser_create = subparsers.add_parser("create-user", help="Create a new user")
    parser_create.add_argument("id", help="User ID")
    parser_create.add_argument("name", help="User Name")

    # list-users command
    subparsers.add_parser("list-users", help="List all users")

    # To handle interactive mode or single command
    if len(sys.argv) > 1:
        args = parser.parse_args()
        _handle_args(app, args)
    else:
        print("Starting interactive CLI... (Type 'exit' to quit)")
        while True:
            try:
                cmd_line = input("cli> ")
                if not cmd_line.strip():
                    continue
                if cmd_line.strip() == "exit":
                    break
                # Parse input as args
                args = parser.parse_args(cmd_line.split())
                _handle_args(app, args)
            except SystemExit:
                # argparse calls sys.exit on error/help in interactive mode
                pass
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

def _handle_args(app: App, args):
    if args.command == "create-user":
        data_transfer_obj = {"id": args.id, "name": args.name}
        user = app.execute(CreateUserCommand, data_transfer_obj)
        print(f"User created: ID={user.id}, Name={user.name}")
    elif args.command == "list-users":
        users = app.query(ListUsersQuery)
        print("Users list:")
        for u in users:
            print(f"  - {u.id}: {u.name}")
