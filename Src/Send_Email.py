import socket
import os
from base64 import b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
from email.header import decode_header

import datetime


def send_email(host, smtp_port, userName, userEmail, userSubject, userContent, toEmails=None, ccEmails=None, bccEmails=None, attachmentFilePaths=None):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, smtp_port))

        recv = client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('220 reply not received from server.')

        heloCommand = 'HELO\r\n'
        client_socket.send(heloCommand.encode())
        recv1 = client_socket.recv(1024).decode()
        print(recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server.')

        msg = MIMEMultipart()
        msg['Message-ID'] = '<' + str(datetime.datetime.now()) + '@' + host + '>'
        msg['User-Agent'] = 'gg team'
        msg['Date'] = formatdate(localtime=True)  
        msg['To'] = ', '.join(toEmails) if toEmails else ''
        msg['From'] = userName + ' <' + userEmail +' >'
        msg['Cc'] = ', '.join(ccEmails) if ccEmails else ''
        msg['Subject'] = userSubject
        body = MIMEText(userContent, 'plain')
        msg.attach(body)

        if attachmentFilePaths:
            for filePath in attachmentFilePaths:
                with open(filePath, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filePath}")
                msg.attach(part)

        fullMessage = msg.as_string().encode()
        client_socket.send(f"MAIL FROM: <{userEmail}>\r\n".encode())
        client_socket.recv(1024)

        for email in (toEmails or []) + (ccEmails or []) + (bccEmails or []):
            client_socket.send(f"RCPT TO: <{email}>\r\n".encode())
            client_socket.recv(1024)

        client_socket.send('DATA\r\n'.encode())
        client_socket.recv(1024)
        client_socket.send(fullMessage)
        client_socket.send("\r\n.\r\n".encode())
        client_socket.recv(1024)

        client_socket.send('QUIT\r\n'.encode())
        client_socket.recv(1024)
        client_socket.close()
        print('Email sent successfully')

    except Exception as e:
        print(f'Error occurred: {e}')