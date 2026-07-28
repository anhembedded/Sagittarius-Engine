import sys
import argparse
from sagittarius_engine.sdk.template_loader import TemplateLoader
from sagittarius_engine.sdk.template_renderer import TemplateRenderer
from sagittarius_engine.sdk.project_generator import ProjectGenerator


def main():
    parser = argparse.ArgumentParser(description="Sagittarius CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: new
    new_parser = subparsers.add_parser(
        "new", help="Create a new project from a template"
    )
    new_parser.add_argument(
        "template", help="Template name (e.g. minimal, clean, ddd, mvc)"
    )
    new_parser.add_argument("project_name", help="Name of the project to create")
    new_parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to create the project in (default: .)",
    )

    args = parser.parse_args()

    if args.command == "new":
        loader = TemplateLoader()
        renderer = TemplateRenderer()
        generator = ProjectGenerator(loader, renderer)

        available_templates = loader.list_templates()
        if args.template not in available_templates:
            print(
                f"Error: Template '{args.template}' not found. Available templates: {', '.join(available_templates)}"
            )
            sys.exit(1)

        try:
            project_path = generator.generate(
                project_name=args.project_name,
                template_name=args.template,
                output_dir=args.output_dir,
            )
            print(
                f"Project '{args.project_name}' created successfully from template '{args.template}' at '{project_path}'."
            )
        except Exception as e:
            print(f"Error generating project: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
