import argparse
import asyncio
from src.infrastructure.Loguru_Logger_infra import LoguruLogger
from src.infrastructure.Silent_Logger_infra import SilentLogger

async def main() -> None:
    # 1. Parse mode
    parser = argparse.ArgumentParser(description="Application Composition Root")
    parser.add_argument(
        "--mode",
        choices=["debug", "release"],
        default="debug",
        help="Environment mode (default: debug)"
    )
    args = parser.parse_args()

    # 2. Init Logger
    if args.mode == "debug":
        logger = LoguruLogger()
    else:
        logger = SilentLogger()

    logger.info(f"Application started in {args.mode} mode")

    # 3. Future steps: Adapters, Use Cases, etc.
    # ...

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
