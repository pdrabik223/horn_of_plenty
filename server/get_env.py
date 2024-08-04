from dotenv import load_dotenv
import os
from typing import Any

load_dotenv()


class EnvVariableNotFound(ValueError):
    pass


def get_env(env_param_name: str) -> Any:
    env_param = os.getenv(env_param_name)
    if env_param is None:
        raise EnvVariableNotFound(env_param_name)
    return env_param
