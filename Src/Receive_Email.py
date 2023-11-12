
import socket
import os
from email import message_from_string, policy
from email.parser import BytesParser
from email.message import *
from email import encoders
def save_processed_id(msg_id):
    """Save the ID of a processed email to a file."""
    with open('processed_ids.txt', 'a') as file:
        file.write(f'{msg_id}\n')

def load_processed_ids():
    PATH = os.path.join(os.getcwd(), 'processed_ids.txt')
    if not os.path.exists(PATH):
        return set()
    with open(PATH, 'r') as file:
        return set(line.strip() for line in file.readlines())

def extract_message_id(email_str):
    """Extract the Message ID from an email."""
    msg = message_from_string(email_str, policy=policy.default)
    return msg['Message-ID']

def get_email_folder_address(email_str):
    """
    Classify an email into a specific folder based on its subject and content.
    This version accepts email as a string in .msg format.

    :param email_str: The email as a string in .msg format.
    :return: The name of the folder where the email should be moved.
    """

    # Parse the email from string
    msg = BytesParser(policy=policy.default).parsebytes(email_str.encode())

    # Extract subject and content from the email
    subject = msg.get('Subject', '').lower()

    content = ''
    if msg.is_multipart():
        for part in msg.get_payload():
            if part.get_payload(decode=True) is not None:
                content += part.get_payload(decode=True).decode()
    else:
        payload = msg.get_payload(decode=True)
        if payload is not None:
            content = payload.decode()

    content = content.lower()

    # Filter for specific senders
    if msg.get('From', '').lower() in ['ahihi@testing.com', 'ahuu@testing.com']:
        return 'Project'

    # Filter for specific subjects
    important_keywords = ['urgent', 'asap']
    if any(keyword in subject for keyword in important_keywords):
        return 'Important'

    # Filter for specific content
    report_keywords = ['report', 'meeting']
    if any(keyword in content for keyword in report_keywords):
        return 'Work'

    # Filter for spam indicators in subject or content
    spam_keywords = ['virus', 'hack', 'crack']
    if any(keyword in subject or keyword in content for keyword in spam_keywords):
        return 'Spam'

    return 'Inbox'

def remove_metadata(email_str):
    """Remove metadata from email response."""
    return '\n'.join(email_str.splitlines()[1:-1])

def receive_email(host, pop3_port, user_email, user_password):
    processed_ids = load_processed_ids()
    try:
        with socket.create_connection((host, pop3_port)) as pop3_client:
            response = pop3_client.recv(1024).decode()
            #print(response)
            pop3_client.sendall(f'USER {user_email}\r\n'.encode())
            response = pop3_client.recv(1024).decode()
            pop3_client.sendall(f'PASS {user_password}\r\n'.encode())
            response = pop3_client.recv(1024).decode()
            #print(response)

            pop3_client.sendall('LIST\r\n'.encode())
            response = pop3_client.recv(1024).decode()
            #print(response)

            pop3_client.sendall('UIDL\r\n'.encode())
            uidl_response = pop3_client.recv(1024).decode()
            uidl_lines = uidl_response.split('\r\n')

            email_count = sum(1 for line in response.split('\r\n') if line and line[0].isdigit())
            for i in range(email_count):
                pop3_client.sendall(f'RETR {i + 1}\r\n'.encode())
                email_response = pop3_client.recv(8192).decode()
                email_response = remove_metadata(email_response)
                #print_email_with_attachment_check(email_response)
                msg_id = extract_message_id(email_response)

                if msg_id and msg_id not in processed_ids:
                    inbox_path = get_email_folder_address(email_response)
                    os.makedirs(inbox_path, exist_ok=True)
                    uidl = uidl_lines[i +1].split(' ')[1].split('.')[0]

                    with open(os.path.join(inbox_path, f'{uidl}.eml'), 'w') as file:
                        file.write(email_response)
                    save_processed_id(msg_id)
                    processed_ids.add(msg_id)

            pop3_client.sendall('QUIT\r\n'.encode())

    except Exception as e:
        print(f'Error with POP3 connection: {e}')