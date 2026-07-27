from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from sagittarius_engine.kernel.context import EngineContext

from sagittarius_engine.interfaces.i_extension import IExtension
from sagittarius_engine.interfaces import IConfig, ILogger
from sagittarius_engine.extensions.persistence.i_session import ISession
from sagittarius_engine.extensions.persistence.sqlalchemy_session_adapter import (
    SQLAlchemySessionAdapter,
)

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    SQLALCHEMY_INSTALLED = True
except ImportError:
    SQLALCHEMY_INSTALLED = False


class DatabaseExtension(IExtension):
    """
    @brief Extension for setting up the Database connection and Session.
    """

    def register(self, context: "EngineContext") -> None:
        logger = self._get_logger(context)
        if not SQLALCHEMY_INSTALLED:
            if logger:
                logger.warning(
                    "DatabaseExtension: sqlalchemy is not installed. Database setup skipped."
                )
            return
        try:
            config: IConfig = context.container.resolve(IConfig)
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
                            "DatabaseExtension: 'database.url' not found. Using default in-memory SQLite."
                        )
        except Exception as e:
            if isinstance(e, ValueError) and "production environment" in str(e):
                raise
            env = str(
                os.environ.get("ENV") or os.environ.get("APP_ENV") or "development"
            ).lower()
            if env == "production":
                raise ValueError(
                    f"Failed to resolve database configuration in production: {e}"
                ) from e
            db_url = "sqlite:///:memory:"
            if logger:
                logger.info(
                    "DatabaseExtension: IConfig not found or failed to resolve. Using default in-memory SQLite."
                )
        try:
            engine = create_engine(db_url)
            session_factory = sessionmaker(bind=engine)
            Session = scoped_session(session_factory)
            session_adapter = SQLAlchemySessionAdapter(Session)
            context.container.singleton(ISession, session_adapter)
            if logger:
                logger.info(
                    f"DatabaseExtension: SQLAlchemy engine created for {db_url} and ISession registered."
                )
        except Exception as e:
            if logger:
                logger.error(f"DatabaseExtension: Failed to initialize database - {e}")

    def boot(self, context: "EngineContext") -> None:
        pass

    def shutdown(self, context: "EngineContext") -> None:
        pass

    def _get_logger(self, context: "EngineContext") -> ILogger | None:
        try:
            return context.container.resolve(ILogger)
        except Exception:
            return None


SqlAlchemyExtension = DatabaseExtension
