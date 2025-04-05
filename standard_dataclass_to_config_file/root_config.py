"""Module for RootConfig."""

from __future__ import annotations

import logging
from pathlib import Path

import mashumaro.codecs.yaml as yaml_codec
import yaml

logger = logging.getLogger(__name__)


class RootConfig:
    """
    Adds the {from_config_filepath} method to any class that inherits this class.
    Thus, any class that has its own config file should inherit this class.
    """

    @classmethod
    def from_config_filepath(cls, config_filepath: Path) -> RootConfig:
        """
        Returns a {RootConfig} from {config_filepath}. If {config_filepath} does not exist, one
        will be created with the default config values.
        """
        if not config_filepath.exists():
            logger.info(
                "The given [%s] does not exist, so creating a default one at that filepath.",
                f"{config_filepath=}",
            )
            default_config = cls()
            config_filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(config_filepath, "w", encoding="utf16") as f:
                f.write(yaml_codec.encode(default_config, cls))
                logger.info("Created default config at [%s].", config_filepath)

            logger.info("Using this config: [%s].", default_config)
            return default_config

        with open(config_filepath, "r", encoding="utf-16") as f:
            config = yaml_codec.decode(str(yaml.safe_load(f)), cls)

            logger.info("Using this config: [%s].", config)
            return config
