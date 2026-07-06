from typing import Any

from src.app_kernel import App
from src.base_module import BaseModule
from src.interfaces import IConfig, ILogger, ISession

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    SQLALCHEMY_INSTALLED = True
except ImportError:
    SQLALCHEMY_INSTALLED = False


class SQLAlchemySessionAdapter(ISession):
    """
    @brief Adapter for SQLAlchemy Session.
    """

    def __init__(self, session: Any):
        self.session = session

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def execute(self, statement: Any, params: Any = None) -> Any:
        return self.session.execute(statement, params)

    def query(self, *entities: Any) -> Any:
        return self.session.query(*entities)

    def add(self, entity: Any) -> None:
        self.session.add(entity)

    def get(self, entity_class: type, entity_id: Any) -> Any | None:
        return self.session.get(entity_class, entity_id)

    def merge(self, entity: Any) -> Any:
        return self.session.merge(entity)

    def delete(self, entity: Any) -> None:
        self.session.delete(entity)

    def close(self) -> None:
        if hasattr(self.session, "remove"):
            self.session.remove()
        elif hasattr(self.session, "close"):
            self.session.close()


class DatabaseModule(BaseModule):
    """
    @brief Module for setting up the Database connection and Session.

    @details This module reads the `database.url` from the configuration.
    If SQLAlchemy is installed, it creates an engine and registers an `ISession`
    singleton in the container using `scoped_session`.

    @par Requirement:
    Requires the `sqlalchemy` package to be installed.

    @par Alembic Tutorial:
    To use Alembic for database migrations:
    1. Run `alembic init alembic` to create a new alembic directory.
    2. Edit `alembic.ini` and set `sqlalchemy.url` to your database URL.
    3. Edit `alembic/env.py` to import your declarative base and set `target_metadata = Base.metadata`.
    4. Run `alembic revision --autogenerate -m "Initial"` to create a migration.
    5. Run `alembic upgrade head` to apply migrations.
    """

    def register(self, app: App) -> None:
        logger = self._get_logger(app)

        if not SQLALCHEMY_INSTALLED:
            if logger:
                logger.warning(
                    "DatabaseModule: sqlalchemy is not installed. Database setup skipped."
                )
            return

        try:
            config: IConfig = app.container.resolve(IConfig)
            import os
            env = str(
                config.get("env")
                or config.get("app.env")
                or os.environ.get("ENV")
                or os.environ.get("APP_ENV")
                or "development"
            ).lower()
            db_url = config.get("database.url")
            if not db_url:
                if env == "production":
                    raise ValueError(
                        "Database configuration 'database.url' is missing in production environment."
                    )
                else:
                    db_url = "sqlite:///:memory:"
                    if logger:
                        logger.info(
                            "DatabaseModule: 'database.url' not found. Using default in-memory SQLite."
                        )
        except Exception as e:
            if isinstance(e, ValueError) and "production environment" in str(e):
                raise
            import os
            env = str(
                os.environ.get("ENV")
                or os.environ.get("APP_ENV")
                or "development"
            ).lower()
            if env == "production":
                raise ValueError(
                    f"Failed to resolve database configuration in production: {e}"
                ) from e
            db_url = "sqlite:///:memory:"
            if logger:
                logger.info(
                    "DatabaseModule: IConfig not found or failed to resolve. Using default in-memory SQLite."
                )

        try:
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)
            Session = scoped_session(session_factory)

            # Create a singleton adapter for the session
            session_adapter = SQLAlchemySessionAdapter(Session)
            app.container.singleton(ISession, session_adapter)

            if logger:
                logger.info(
                    f"DatabaseModule: SQLAlchemy engine created for {db_url} and ISession registered."
                )
        except Exception as e:
            if logger:
                logger.error(f"DatabaseModule: Failed to initialize database - {e}")

    def boot(self, app: App) -> None:
        pass

    def _get_logger(self, app: App) -> ILogger | None:
        try:
            return app.container.resolve(ILogger)
        except Exception:
            return None
