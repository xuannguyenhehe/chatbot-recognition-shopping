import yaml
import re
from ..constants import CFG_FLOAT_KEYS, CFG_FRACTION_KEYS, CFG_INT_KEYS, CFG_BOOL_KEYS

class Config(dict): 
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            name = self.__class__.__name__
            raise AttributeError(f"'{name}' object has no attribute '{attr}'")

def yaml_load(file_name: str):
    with open(file_name, errors='ignore', encoding='utf-8') as f:
        # Add YAML filename to dict and return
        s = f.read()  # string
        if not s.isprintable():  # remove special characters
            s = re.sub(r'[^\x09\x0A\x0D\x20-\x7E\x85\xA0-\uD7FF\uE000-\uFFFD\U00010000-\U0010ffff]+', '', s)
        return yaml.safe_load(s)
    
def get_cfg(cfg_name: str)-> Config:
    cfg = yaml_load(cfg_name)

    # Check key, value of config
    for key, value in cfg.items():
        if value is not None:  # None values may be from optional args
            if key in CFG_FLOAT_KEYS and not isinstance(value, (int, float)):
                raise TypeError(f"'{key}={value}' is of invalid type {type(value).__name__}. "
                                f"Valid '{key}' types are int (i.e. '{key}=0') or float (i.e. '{key}=0.5')")
            elif key in CFG_FRACTION_KEYS:
                if not isinstance(value, (int, float)):
                    raise TypeError(f"'{key}={value}' is of invalid type {type(value).__name__}. "
                                    f"Valid '{key}' types are int (i.e. '{key}=0') or float (i.e. '{key}=0.5')")
                if not (0.0 <= value <= 1.0):
                    raise ValueError(f"'{key}={value}' is an invalid value. "
                                     f"Valid '{key}' values are between 0.0 and 1.0.")
            elif key in CFG_INT_KEYS and not isinstance(value, int):
                raise TypeError(f"'{key}={value}' is of invalid type {type(value).__name__}. "
                                f"'{key}' must be an int (i.e. '{key}=8')")
            elif key in CFG_BOOL_KEYS and not isinstance(value, bool):
                raise TypeError(f"'{key}={value}' is of invalid type {type(value).__name__}. "
                                f"'{key}' must be a bool (i.e. '{key}=True' or '{key}=False')")
    return Config(cfg)