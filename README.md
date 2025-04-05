# Standard Dataclass to Config File
I like to use yaml config files in my projects, but having to copy paste the parsing/saving logic was annoying.

# Example Usage
```python
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from standard_dataclass_to_config_file.root_config import RootConfig


@dataclass
class YoutubeApiConfig:
    api_key: str = ""


@dataclass
class DownloadConfig:
    youtube_api: YoutubeApiConfig = field(default_factory=YoutubeApiConfig)
    thread_limit: int = 5


@dataclass
class Config(RootConfig):
    download: DownloadConfig = field(default_factory=DownloadConfig)
    logs_dirname: str = ""


CONFIG = Config.from_config_filepath(Path("./config/config.yaml"))

print(yaml.dump(CONFIG))
```

On first run without a config file, this creates the config file at the given filepath of `./config/config.yaml` with following the contents (as well as prints this to console):
```yaml
download:
  thread_limit: 5
  youtube_api:
    api_key: ''
logs_dirname: ''
```

Now, if we change the contents of that file `./config/config.yaml` to look like:
```yaml
download:
  thread_limit: 1234567890
  youtube_api:
    api_key: 'random api key that is not the default'
logs_dirname: 'random-logs-dirname'
```

then the script will print out:
```yaml
download:
  thread_limit: 1234567890
  youtube_api:
    api_key: random api key that is not the default
logs_dirname: random-logs-dirname
```
