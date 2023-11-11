import socket
import os
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header

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
        print(response)

        # Process each email (example: fetching the first email)
        pop3_client.sendall('RETR 1\r\n'.encode())
        response = pop3_client.recv(1024).decode()
        print(response)

        # Close the connection
        pop3_client.sendall('QUIT\r\n'.encode())
        pop3_client.close()
    except Exception as e:
        print(f'Lỗi kết nối POP3: {e}')
