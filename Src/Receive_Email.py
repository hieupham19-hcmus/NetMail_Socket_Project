import socket
import os
from email.parser import BytesParser
from email import policy

def receive_email(host, pop3_port, user_email, user_password):
    try:
        # Establish connection to the server
        with socket.create_connection((host, pop3_port)) as pop3_client:
            print(pop3_client.recv(1024).decode())  # Server greeting

            # Send USER and PASS commands
            pop3_client.sendall(f'USER {user_email}\r\n'.encode())
            print(pop3_client.recv(1024).decode())

            pop3_client.sendall(f'PASS {user_password}\r\n'.encode())
            print(pop3_client.recv(1024).decode())

            # Retrieve list of emails
            pop3_client.sendall('LIST\r\n'.encode())
            response = pop3_client.recv(1024).decode()
            print(response)
            
            pop3_client.sendall('UIDL\r\n'.encode())
            uidl_response = pop3_client.recv(1024).decode()
            uidl_lines = uidl_response.split('\r\n')
            
            # Process each email
            email_count = sum(1 for line in response.split('\r\n') if line and line[0].isdigit())
            for i in range(email_count):
                pop3_client.sendall(f'RETR {i + 1}\r\n'.encode())
                email_response = pop3_client.recv(16384).decode()
                
                # Save email to appropriate directory
                inbox_path = get_email_folder_address(email_response)
                os.makedirs(inbox_path, exist_ok=True)
                uidl = uidl_lines[i+1].split(' ')[1].split('.')[0]
                
                with open(os.path.join(inbox_path, f'{uidl}.eml'), 'w') as file:
                    file.write(remove_metadata(email_response))

            # Close the connection
            pop3_client.sendall('QUIT\r\n'.encode())

    except Exception as e:
        print(f'Error with POP3 connection: {e}')

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
    if msg.is_multipart():
        content = ''.join(part.get_payload(decode=True).decode() for part in msg.get_payload())
    else:
        content = msg.get_payload(decode=True).decode()
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
