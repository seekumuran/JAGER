from abc import ABC, abstractmethod


class Target(ABC):
    """
    Abstract interface for anything JÄGER can explore.

    The target can eventually be:
        - the Python black-box simulator
        - a Linux system
        - an AI sandbox
        - another executable
        - a remote test environment

    JÄGER's reasoning layer should not need to know
    which target it is interacting with.
    """

    @abstractmethod
    def observe(self, **inputs):
        """
        Execute an observation against the target.

        Returns a dictionary containing:
            inputs
            telemetry
            status
        """
        raise NotImplementedError


class TargetCapabilities:

    def __init__(
        self,
        name,
        version,
        description,
    ):
        self.name = name
        self.version = version
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
        }
