import json
import sys
import datetime


def get_info_from_config(config_path: str, attribute: str):
    try:
        config = json.load(open(config_path))
        return config[attribute]

    except FileNotFoundError as e:
        print(f"bad filepath {config_path}")
        sys.exit(1)

    except json.decoder.JSONDecodeError as e:
        print(f"json parsing failed {e}")
        sys.exit(2)

    except Exception as e:
        print(f"unexpected error while parsing config {e}")
        sys.exit(-1)