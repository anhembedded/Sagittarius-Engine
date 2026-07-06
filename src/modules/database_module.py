from typing import Optional, Any
from src.base_module import BaseModule
from src.app_kernel import App
from src.interfaces import IConfig, ILogger, ISession

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
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
                logger.warning("DatabaseModule: sqlalchemy is not installed. Database setup skipped.")
            return

        try:
            config: IConfig = app.container.resolve(IConfig)
            db_url = config.get("database.url", "sqlite:///:memory:")
        except Exception:
            db_url = "sqlite:///:memory:"
            if logger:
                logger.info("DatabaseModule: IConfig not found or failed to resolve. Using default in-memory SQLite.")

        try:
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)
            Session = scoped_session(session_factory)

            # Create a singleton adapter for the session
            session_adapter = SQLAlchemySessionAdapter(Session)
            app.container.singleton(ISession, session_adapter)

            if logger:
                logger.info(f"DatabaseModule: SQLAlchemy engine created for {db_url} and ISession registered.")
        except Exception as e:
            if logger:
                logger.error(f"DatabaseModule: Failed to initialize database - {e}")

    def boot(self, app: App) -> None:
        pass

    def _get_logger(self, app: App) -> Optional[ILogger]:
        try:
            return app.container.resolve(ILogger)
        except Exception:
            return None
