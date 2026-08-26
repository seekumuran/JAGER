from typing import Any, Callable, Dict, Optional

from .action import Action
from .action_authorizer import (
    ActionAuthorizer,
)


class ActionDispatcher:

    def __init__(
        self,
        authorizer: ActionAuthorizer,
    ):

        self.authorizer = authorizer

        self._handlers: Dict[
            str,
            Callable,
        ] = {}

    def register(
        self,
        action_type: str,
        handler: Callable,
    ):

        if not callable(handler):

            raise TypeError(
                "handler must be callable"
            )

        self._handlers[
            action_type
        ] = handler

        return handler

    def unregister(
        self,
        action_type: str,
    ):

        return self._handlers.pop(
            action_type,
            None,
        )

    def dispatch(
        self,
        action: Action,
    ):

        authorization = (
            self.authorizer.authorize(
                action
            )
        )

        if not authorization[
            "allowed"
        ]:

            return {
                "success": False,
                "authorization":
                    authorization,
                "output": None,
            }

        handler = self._handlers.get(
            action.action_type
        )

        if handler is None:

            return {
                "success": False,
                "authorization":
                    authorization,
                "output": None,
                "error":
                    "no handler registered",
            }

        try:

            output = handler(
                action
            )

            return {
                "success": True,
                "authorization":
                    authorization,
                "output": output,
            }

        except Exception as exc:

            return {
                "success": False,
                "authorization":
                    authorization,
                "output": None,
                "error": str(exc),
            }
