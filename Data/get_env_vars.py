from dataclasses import dataclass
from dotenv import load_dotenv, dotenv_values

load_dotenv()
env_vars = dotenv_values('Data/.env')
@dataclass
class GetEnvVars:
    map_box_key: str = env_vars['MAPBOX_KEY']
    
