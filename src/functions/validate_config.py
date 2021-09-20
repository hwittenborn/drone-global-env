def validate_config():
    import os
    import yaml

    from functions.lint_config import lint_config

    config_path = os.environ.get("CONFIG_FILE", "/data/config.yaml")

    if os.path.exists(config_path) is False:
        print("[Error] Couldn't find config file.")
        print(f"[Error] Make sure '{config_path}' exists and try again.")
        exit(1)

    try:
        file = open(config_path, "r")
        config_data = file.read()
        file.close()
    except PermissionError:
        print("[Error] Couldn't read the configuration file.")
        exit(1)

    try:
        loaded_config_data = yaml.load(config_data, Loader=yaml.SafeLoader)
    except yaml.scanner.ScannerError:
    	print("[Error] Your configuration file doesn't appear to have valid syntax.")
    	quit(1)

    lint_config(loaded_config_data)

    return loaded_config_data
