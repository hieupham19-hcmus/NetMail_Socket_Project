import base64
import socket
import os
from email import message_from_string, policy
from email.parser import BytesParser
from email.message import *
from email import encoders
from filter import filter
import email
import quopri
import sqlite3


def save_processed_id(msg_id):
    # Database connection
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # SQL command to insert data
    insert_command = "INSERT INTO message_status (message_id, status) VALUES (?, 0)"

    try:
        # Execute the command
        cursor.execute(insert_command, (msg_id,))
        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()


def load_processed_ids():
    processed_ids = set()

    # Database connection
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # SQL command to select all message IDs
    select_command = "SELECT message_id FROM message_status"

    try:
        # Execute the command and fetch all results
        cursor.execute(select_command)
        rows = cursor.fetchall()

        # Add each message ID to the set
        for row in rows:
            processed_ids.add(row[0])
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return processed_ids


def extract_message_id(email_str):
    """Extract the Message ID from an email."""
    msg = message_from_string(email_str, policy=policy.default)
    return msg['Message-ID']


def remove_metadata(email_str):
    """Remove metadata from email response."""
    return '\n'.join(email_str.splitlines()[1:])


def process_email(raw_email_bytes):
    """Process email bytes, decode attachments, and return the full email content and attachments."""
    msg = BytesParser(policy=policy.default).parsebytes(raw_email_bytes)

    # Walk through the parts of the email to find attachments
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get("Content-Disposition", None)
            if content_disposition and "attachment" in content_disposition:
                # Extract the filename and the content transfer encoding
                filename = part.get_filename()
                cte = part.get("Content-Transfer-Encoding")

                # Decode the attachment based on its Content-Transfer-Encoding
                if cte == 'base64':
                    binary_content = part.get_payload(decode=True)
                elif cte == 'quoted-printable':
                    binary_content = quopri.decodestring(part.get_payload())
                elif cte == '7bit' or cte == '8bit' or cte == 'binary':
                    binary_content = part.get_payload(decode=True)
                else:
                    # If encoding is unknown or not provided, we keep the payload as is
                    binary_content = part.get_payload()

    full_email_str = msg.as_string()

    return full_email_str


def receive_full_email(pop3_client):
    """Receive the full content of an email from the socket as bytes, stripping POP3 response lines."""
    email_response = []
    while True:
        chunk = pop3_client.recv(8192)
        if chunk.startswith(b'+OK'):  # Handle the initial POP3 response line
            # Find the end of the line and start collecting from the next line
            end_of_ok_line = chunk.find(b'\r\n') + 2  # Add 2 for the length of '\r\n'
            chunk = chunk[end_of_ok_line:]

        if chunk.endswith(b'\r\n.\r\n'):  # End of email transmission in POP3
            email_response.append(chunk[:-5])  # Remove the termination sequence
            break
        else:
            email_response.append(chunk)
    return b''.join(email_response)


def receive_email(host, pop3_port, user_email, user_password, config):
    """Receive emails from a POP3 server."""
    processed_IDs = load_processed_ids()
    try:
        with socket.create_connection((host, pop3_port)) as pop3_client:
            pop3_client.recv(1024)
            pop3_client.sendall(f'USER {user_email}\r\n'.encode())
            pop3_client.recv(1024)  # User OK
            pop3_client.sendall(f'PASS {user_password}\r\n'.encode())
            pop3_client.recv(1024)  # Pass OK

            pop3_client.sendall('LIST\r\n'.encode())
            response = pop3_client.recv(1024).decode()

            pop3_client.sendall('UIDL\r\n'.encode())
            UIDL_Response = pop3_client.recv(1024).decode()
            UIDL_Lines = UIDL_Response.split('\r\n')

            email_count = sum(1 for line in response.split('\r\n') if line and line[0].isdigit())

            for i in range(email_count):
                pop3_client.sendall(f'RETR {i + 1}\r\n'.encode())
                email_response = receive_full_email(pop3_client)
                modified_email = process_email(email_response)
                MSG_ID = extract_message_id(modified_email)

                if MSG_ID and MSG_ID not in processed_IDs:
                    #D:\NetMail_Socket_Project\Src\Inbox
                    inbox_path = 'Email\\' + filter(modified_email, config)
                    os.makedirs(inbox_path, exist_ok=True)
                    UIDL = UIDL_Lines[i + 1].split(' ')[1].split('.')[0]
                    with open(os.path.join(inbox_path, f'{UIDL}.eml'), 'w') as file:
                        file.write(modified_email)
                    save_processed_id(MSG_ID)
                    processed_IDs.add(MSG_ID)

            pop3_client.sendall('QUIT\r\n'.encode())

    except Exception as e:
        print(f'Error with POP3 connection: {e}')
