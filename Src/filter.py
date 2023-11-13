from email import policy
from email.parser import BytesParser
from email.message import *


def filter(email):
    sender_keywords = ['ahihi@testing.com', 'ahuu@testing.com']
    important_keywords = ['urgent', 'asap']
    report_keywords = ['report', 'meeting']
    spam_keywords = ['virus', 'hack', 'crack']

    # Check if email is an instance of EmailMessage
    if not isinstance(email, EmailMessage):
        msg = BytesParser(policy=policy.default).parsebytes(email.encode())
    else:
        msg = email

    subject = msg.get('Subject', '').lower()

    content = ''
    if msg.is_multipart():
        for part in msg.get_payload():
            # Check if part is a text type before decoding
            if part.get_content_type() in ['text/plain', 'text/html']:
                payload = part.get_payload(decode=True)
                if payload is not None:
                    content += payload.decode()
    else:
        payload = msg.get_payload(decode=True)
        if payload is not None:
            content = payload.decode()

    content = content.lower()

    # Filter for specific senders
    if msg.get('From', '').lower() in sender_keywords:
        return 'Project'

    # Filter for specific subjects
    if any(keyword in subject for keyword in important_keywords):
        return 'Important'

    # Filter for specific content
    if any(keyword in content for keyword in report_keywords):
        return 'Work'

    # Filter for spam indicators in subject or content
    if any(keyword in subject or keyword in content for keyword in spam_keywords):
        return 'Spam'

    return 'Inbox'
