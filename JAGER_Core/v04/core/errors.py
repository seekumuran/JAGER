class JagerError(Exception):
    """Base exception for JAGER."""


class ConfigurationError(JagerError):
    """Raised when JAGER configuration is invalid."""


class ExecutionError(JagerError):
    """Raised when execution fails."""


class StateError(JagerError):
    """Raised when an invalid state transition occurs."""


class ComponentError(JagerError):
    """Raised when a required component is unavailable."""
