def set_environment():
    env_path = "../.env"
    try:
        with open(env_path, "r") as f:
            for line in f:
                if '=' in line and not line.strip().startswith("#"):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        return
