import os


def set_environment(path: str = None):
    env_path = "../.env"
    if path is not None:
        env_path = path
    try:
        with open(env_path, "r") as f:
            for line in f:
                if '=' in line and not line.strip().startswith("#"):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        return
