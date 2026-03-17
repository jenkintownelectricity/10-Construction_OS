"""Runtime logger.

Simple append-oriented runtime logging for tracking parser events,
validation outcomes, engine actions, deliverable generation events,
and pipeline outputs.
"""

import logging
from typing import Any


class RuntimeLogger:
    """Append-oriented logger for Construction Runtime events."""

    def __init__(self, name: str = "construction_runtime"):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG)

        self._events: list[dict[str, Any]] = []

    def log_parser_event(self, parser_name: str, status: str, details: str = "") -> None:
        """Log a parser event."""
        entry = {"category": "parser", "parser": parser_name, "status": status, "details": details}
        self._events.append(entry)
        self._logger.info("Parser [%s]: %s — %s", parser_name, status, details)

    def log_validation(self, is_valid: bool, warnings: list[str], errors: list[str]) -> None:
        """Log a validation outcome."""
        entry = {"category": "validation", "is_valid": is_valid, "warnings": warnings, "errors": errors}
        self._events.append(entry)
        level = logging.INFO if is_valid else logging.WARNING
        self._logger.log(level, "Validation: valid=%s, warnings=%d, errors=%d", is_valid, len(warnings), len(errors))

    def log_engine_action(self, engine_name: str, action: str, details: str = "") -> None:
        """Log an engine action."""
        entry = {"category": "engine", "engine": engine_name, "action": action, "details": details}
        self._events.append(entry)
        self._logger.info("Engine [%s]: %s — %s", engine_name, action, details)

    def log_generation(self, deliverable_type: str, status: str, details: str = "") -> None:
        """Log a deliverable generation event."""
        entry = {"category": "generation", "deliverable_type": deliverable_type, "status": status, "details": details}
        self._events.append(entry)
        self._logger.info("Generator [%s]: %s — %s", deliverable_type, status, details)

    def log_pipeline(self, step: str, status: str, details: str = "") -> None:
        """Log a pipeline output/step."""
        entry = {"category": "pipeline", "step": step, "status": status, "details": details}
        self._events.append(entry)
        self._logger.info("Pipeline [%s]: %s — %s", step, status, details)

    def get_events(self) -> list[dict[str, Any]]:
        """Return all logged events."""
        return list(self._events)
