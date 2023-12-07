import json
import xml.etree.ElementTree as ET


def read_config_file(filepath):
    # Dictionary to store the configuration
    config = {}

    try:
        if filepath.endswith('.json'):
            # JSON format
            with open(filepath, 'r') as file:
                config = json.load(file)

        elif filepath.endswith('.xml'):
            # XML format
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

        elif filepath.endswith('.txt'):
            with open(filepath, 'r') as file:
                section = None
                filter_section = None
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    if line.endswith(':'):
                        section = line[:-1].lower()
                        if section == 'filters':
                            config[section] = []
                        else:
                            config[section] = {}
                    elif ':' in line and section:
                        key, value = line.split(':', 1)
                        key, value = key.strip(), value.strip()
                        if section == 'filters':
                            if key == 'Filter':
                                if filter_section:
                                    config[section].append(filter_section)
                                filter_section = {}
                            elif filter_section is not None:
                                if key == 'Keywords':
                                    filter_section['keywords'] = []
                                elif key == 'Keyword':
                                    filter_section['keywords'].append(value)
                                else:
                                    filter_section[key.lower()] = value
                        else:
                            config[section][key] = value
                if filter_section:
                    config['filters'].append(filter_section)

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

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

    return config
