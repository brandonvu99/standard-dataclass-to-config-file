"""Module for RootConfigTest."""

import tempfile
import unittest
from dataclasses import dataclass, field
from pathlib import Path

from assertpy import assert_that

from standard_dataclass_to_config_file.root_config import RootConfig


class RootConfigTest(unittest.TestCase):
    """
    Unit tests for RootConfig.
    """

    def test__from_config_filepath__filepath_does_not_exist__saves_default_config_to_filepath(
        self,
    ):
        with tempfile.TemporaryDirectory() as dirname:
            config_filename = "test-config.yaml"
            config_filepath = Path(dirname) / config_filename

            actual_config = RootTestConfig.from_config_filepath(config_filepath)

            with open(config_filepath, "r", encoding="utf16") as f:
                file_lines = f.read()
                assert_that(file_lines).is_equal_to(
                    "\n".join(
                        [
                            "download:",
                            "  thread_limit: 5",
                            "  youtube_api:",
                            "    api_key: ''",
                            "logs_dirname: ''",
                            "",
                        ]
                    )
                )
            assert_that(actual_config).is_equal_to(
                RootTestConfig(DownloadTestConfig(YoutubeApiTestConfig()))
            )

    def test__from_config_filepath__filepath_does_exist__loads_from_filepath(
        self,
    ):
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(
                bytes(
                    "\n".join(
                        [
                            "download:",
                            "  thread_limit: 692371348",
                            "  youtube_api:",
                            "    api_key: 'random api key that is not the default'",
                            "logs_dirname: 'random-logs-dirname'",
                        ]
                    ),
                    encoding="utf16",
                )
            )
            fp.seek(0)

            actual_config = RootTestConfig.from_config_filepath(Path(fp.name))

            assert_that(actual_config).is_equal_to(
                RootTestConfig(
                    DownloadTestConfig(
                        thread_limit=692371348,
                        youtube_api=YoutubeApiTestConfig(
                            api_key="random api key that is not the default"
                        ),
                    ),
                    logs_dirname="random-logs-dirname",
                )
            )


@dataclass
class YoutubeApiTestConfig:
    """
    Test config.
    """

    api_key: str = ""


@dataclass
class DownloadTestConfig:
    """
    Test config.
    """

    youtube_api: YoutubeApiTestConfig = field(default_factory=YoutubeApiTestConfig)
    thread_limit: int = 5


@dataclass
class RootTestConfig(RootConfig):
    """
    Test config.
    """

    download: DownloadTestConfig = field(default_factory=DownloadTestConfig)
    logs_dirname: str = ""
