class TargetAdapter:
    """
    Generic interface between JÄGER and a target.

    A real Linux target, sandbox, simulator,
    or external system can implement this
    interface without changing the hunter.
    """

    def observe(self, **inputs):
        raise NotImplementedError(
            "Target adapters must implement observe()."
        )


class CallableTargetAdapter(TargetAdapter):
    def __init__(self, function):
        self.function = function

    def observe(self, **inputs):
        return self.function(**inputs)
