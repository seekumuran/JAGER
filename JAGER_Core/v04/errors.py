class JagerError(Exception):
    """Base JÄGER exception."""


class InvalidActionError(JagerError):
    """Raised when an action is invalid."""


class UnsafeActionError(JagerError):
    """Raised when an action violates safety policy."""


class InvalidObservationError(JagerError):
    """Raised when a target returns invalid telemetry."""


class ConfigurationError(JagerError):
    """Raised when configuration is invalid."""
