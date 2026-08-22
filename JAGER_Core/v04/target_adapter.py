from .target import Target


class TargetAdapter(Target):
    """
    Compatibility layer for targets that already expose
    an observe() method.

    This keeps the existing adapter API while making it
    conform to JÄGER's target abstraction.
    """

    def observe(self, **inputs):
        raise NotImplementedError(
            "Target adapters must implement observe()."
        )


class CallableTargetAdapter(TargetAdapter):

    def __init__(self, function):
        self.function = function

    def observe(self, **inputs):
        return self.function(
            **inputs
        )
