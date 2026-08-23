from typing import Any, Callable, Optional


class JagerExecutor:

    def __init__(
        self,
        handler: Optional[
            Callable[[Any], Any]
        ] = None,
    ):

        self.handler = handler

    def set_handler(
        self,
        handler: Callable[[Any], Any],
    ):

        if not callable(handler):

            raise TypeError(
                "handler must be callable"
            )

        self.handler = handler

    def execute(
        self,
        action: Any,
    ):

        if self.handler is None:

            return action

        return self.handler(
            action
        )
