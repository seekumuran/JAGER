from pathlib import Path
from typing import Any, Dict, Optional

from .config.loader import ConfigLoader
from .config.resolver import ConfigResolver
from .core.config import JagerConfig
from .core.facade import Jager


class JagerBootstrap:

    def __init__(
        self,
        config_path: Optional[str] = None,
        overrides: Optional[
            Dict[str, Any]
        ] = None,
    ):

        self.config_path = config_path
        self.overrides = overrides or {}

        self.loader = ConfigLoader()
        self.resolver = ConfigResolver()

        self.config: Optional[
            JagerConfig
        ] = None

        self.jager: Optional[
            Jager
        ] = None

    def load_config(self):

        if self.config_path:

            config = self.loader.load_file(
                self.config_path
            )

        else:

            config = self.loader.load_default()

        self.config = self.resolver.resolve(
            config=config,
            overrides=self.overrides,
        )

        return self.config

    def build(self):

        if self.config is None:

            self.load_config()

        self.jager = Jager(
            self.config
        )

        return self.jager

    def initialize(self):

        if self.jager is None:

            self.build()

        self.jager.start()

        return self.jager

    def data_directory(self):

        if self.config is None:

            self.load_config()

        path = Path(
            self.config.data_directory
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path


def bootstrap(
    config_path: Optional[str] = None,
    overrides: Optional[
        Dict[str, Any]
    ] = None,
):

    runtime = JagerBootstrap(
        config_path=config_path,
        overrides=overrides,
    )

    return runtime.initialize()
