import os
import json
import sys
import yaml


class ConfigNamespace:
    """
    A helper class that turns a dictionary into an object with attribute-style access.
    Recursively turns nested dictionaries into ConfigNamespace instances.
    """

    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = ConfigNamespace(value)
            self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def to_dict(self):
        """
        Converts the ConfigNamespace (recursively) back to a plain dictionary.
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigNamespace):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def __repr__(self):
        return f"Config({self.__dict__})"

    def __str__(self):
        """
        Pretty YAML-like string representation of the config.
        """
        return yaml.dump(self.to_dict(), sort_keys=False, default_flow_style=False)

    def to_string(self):
        """
        Returns the config as a formatted string (same as __str__).
        """
        return str(self)


class Config(ConfigNamespace):

    """
    Load a configuration file (YAML or JSON) and allow attribute-style access.
    """
    def __init__(self, path):
        if not os.path.exists(path):
            print(f"[ERROR] Config file '{path}' does not exist.")
            sys.exit(1)

        try:
            with open(path, "r", encoding="utf-8") as f:
                if path.endswith(".yaml") or path.endswith(".yml"):
                    data = yaml.safe_load(f)
                elif path.endswith(".json"):
                    data = json.load(f)
                else:
                    print("[ERROR] Unsupported config file format. Use .yaml, .yml or .json")
                    sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Failed to read config file: {e}")
            sys.exit(1)

        if not isinstance(data, dict):
            print("[ERROR] Configuration file must contain a dictionary at the top level.")
            sys.exit(1)

        super().__init__(data)
