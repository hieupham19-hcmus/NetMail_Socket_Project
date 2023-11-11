import socket
import os
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header
from email import policy
from email.parser import BytesParser

def receive_email(host, pop3_port, userEmail, userPassword):
    try:
        pop3_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pop3_client.connect((host, pop3_port))
        
        # Receive server greeting
        response = pop3_client.recv(1024).decode()
        print(response)
        
        # Send USER command
        pop3_client.sendall(f'USER {userEmail}\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        print(response)

        # Send PASS command
        pop3_client.sendall(f'PASS {userPassword}\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        print(response)

        # Send LIST command to get list of emails
        pop3_client.sendall('LIST\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        lines = response.split('\r\n')
        email_count = sum(1 for line in lines if line and line[0].isdigit())
        print(response)
        
        pop3_client.sendall('UIDL\r\n'.encode())
        uidl_response = pop3_client.recv(1024).decode()
        uidl_lines = uidl_response.split('\r\n')
        
        for i in range(email_count):
            uidl = uidl_lines[i+1].split(' ')[1]
            pop3_client.sendall(f'RETR {i+1}\r\n'.encode())
            
            response = pop3_client.recv(16384).decode()
            # save to pathfolder
            current_directory = os.getcwd()
            # Add filer
            inbox_path = os.path.join(current_directory, classify_email(response))
            os.makedirs(inbox_path, exist_ok=True)
            with open(f'{inbox_path}/{uidl}', 'w') as f:
                f.write(response)

        # Close the connection
        pop3_client.sendall('QUIT\r\n'.encode())
        pop3_client.close()
    except Exception as e:
        print(f'Lỗi kết nối POP3: {e}')
   
def receive_email(host, pop3_port, userEmail, userPassword):
    try:
        pop3_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pop3_client.connect((host, pop3_port))
        
        # Receive server greeting
        response = pop3_client.recv(1024).decode()
        print(response)
        
        # Send USER command
        pop3_client.sendall(f'USER {userEmail}\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        print(response)

        # Send PASS command
        pop3_client.sendall(f'PASS {userPassword}\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        print(response)

        # Send LIST command to get list of emails
        pop3_client.sendall('LIST\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        lines = response.split('\r\n')
        email_count = sum(1 for line in lines if line and line[0].isdigit())
        print(response)
        
        pop3_client.sendall('UIDL\r\n'.encode())
        uidl_response = pop3_client.recv(1024).decode()
        uidl_lines = uidl_response.split('\r\n')
        
        for i in range(email_count):
            uidl = uidl_lines[i+1].split(' ')[1]
            pop3_client.sendall(f'RETR {i+1}\r\n'.encode())
            
            response = pop3_client.recv(16384).decode()
            # save to pathfolder
            current_directory = os.getcwd()
            # Add filer
            inbox_path = os.path.join(current_directory, classify_email(response))
            os.makedirs(inbox_path, exist_ok=True)
            uidl = uidl.split('.')[0]
            response = remove_first_last_lines(response)
            with open(f'{inbox_path}/{uidl}.eml', 'w') as f:
                f.write(response)

        # Close the connection
        pop3_client.sendall('QUIT\r\n'.encode())
        pop3_client.close()
    except Exception as e:
        print(f'Error with POP3 connection: {e}')

def remove_first_last_lines(text):
    lines = text.splitlines()
    modified_lines = lines[1:-1]
    return "\n".join(modified_lines)

def classify_email(email_str):
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
 
  
