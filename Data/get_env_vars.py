from dataclasses import dataclass
from dotenv import dotenv_values

env_vars = dotenv_values('Data/.env')
@dataclass
class GetEnvVars:
    map_box_key: str = env_vars['MAPBOX_KEY']
    
