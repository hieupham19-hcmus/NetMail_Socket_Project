import json
import xml.etree.ElementTree as ET
import configparser


## chua check .cfg va .ini
def read_config_file(filepath):
    # Dictionary to store the configuration
    config = {}

    # Determine the file extension to decide the parsing strategy
    if filepath.endswith('.xml'):
        # XML format
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            if root.tag != 'config':
                raise ValueError("Root element is not 'config'")
            for child in root:
                config[child.tag] = child.text
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
            return None

    elif filepath.endswith('.cfg') or filepath.endswith('.ini'):
        # CFG or INI format
        try:
            parser = configparser.ConfigParser()
            parser.read(filepath)
            # Assuming the configuration is under a 'default' section
            if 'default' in parser:
                for key in parser['default']:
                    config[key] = parser['default'][key]
            else:
                # Handle case where there's no 'default' section
                for section in parser.sections():
                    for key, value in parser.items(section):
                        config[key] = value
        except configparser.Error as e:
            print(f"ConfigParser Error: {e}")
            return None

    elif filepath.endswith('.json'):
        # JSON format
        try:
            with open(filepath, 'r') as file:
                config = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return None
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return None

    elif filepath.endswith('.txt'):
        # TXT format (or default)
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        config[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None

    else:
        print(f"Error: Unsupported file extension: {filepath}")

    # Check if all required keys are present
    required_keys = ['Username', 'Password', 'MailServer', 'SMTP', 'POP3', 'AutoLoad']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    return config
