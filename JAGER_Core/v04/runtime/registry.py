from typing import Any, Dict, Optional


class ComponentRegistry:

    def __init__(self):

        self._components: Dict[
            str,
            Any,
        ] = {}

    def register(
        self,
        name: str,
        component: Any,
        *,
        replace: bool = False,
    ):

        if (
            name in self._components
            and not replace
        ):
            raise KeyError(
                f"component already "
                f"registered: {name}"
            )

        self._components[name] = (
            component
        )

        return component

    def get(
        self,
        name: str,
        default: Optional[Any] = None,
    ):

        return self._components.get(
            name,
            default,
        )

    def require(
        self,
        name: str,
    ):

        component = self.get(name)

        if component is None:

            raise KeyError(
                f"unknown component: "
                f"{name}"
            )

        return component

    def remove(
        self,
        name: str,
    ):

        return self._components.pop(
            name,
            None,
        )

    def contains(
        self,
        name: str,
    ):

        return name in self._components

    def names(self):

        return list(
            self._components.keys()
        )

    def values(self):

        return list(
            self._components.values()
        )

    def snapshot(self):

        return {
            name: type(component).__name__
            for name, component
            in self._components.items()
        }
