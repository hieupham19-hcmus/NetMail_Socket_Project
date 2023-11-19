import json
import xml.etree.ElementTree as ET


def read_config_file(filepath):
    # Dictionary to store the configuration
    config = {}

    if filepath.endswith('.json'):
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

    elif filepath.endswith('.xml'):
        # XML format
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            for child in root:
                if child.tag == 'General':
                    config['general'] = {subchild.tag: subchild.text for subchild in child}
                elif child.tag == 'Filters':
                    config['filters'] = []
                    for subchild in child:
                        filter_dict = {}
                        for element in subchild:
                            if element.tag == 'Keywords':
                                filter_dict['keywords'] = [keyword.text for keyword in element]
                            elif element.tag == 'ApplyTo':
                                filter_dict['applyTo'] = [apply.text for apply in element]
                            else:
                                filter_dict[element.tag.lower()] = element.text
                        config['filters'].append(filter_dict)
        except ET.ParseError as e:
            print(f"XML Parse Error: {e}")
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
        return None

    # Validation for all file types
    required_keys = ['Username', 'Password', 'MailServer', 'SMTP', 'POP3', 'AutoLoad']
    if 'general' in config:
        for key in required_keys:
            if key not in config['general']:
                raise ValueError(f"Missing required key in 'general' section: {key}")
    else:
        print("Error: 'general' section missing in the configuration file.")
        return None

    return config
