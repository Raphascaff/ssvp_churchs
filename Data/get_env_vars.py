import os
from dataclasses import dataclass


@dataclass
class GetEnvVars:
    map_box_key: str = os.getenv('MAPBOX_KEY', 'default_value')
