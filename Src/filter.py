from email import policy
from email.parser import BytesParser
from email.message import *


def filter(email, config):
    if not isinstance(email, EmailMessage):
        email = BytesParser(policy=policy.default).parsebytes(email.encode())

    subject = email.get('Subject', '').lower()
    from_field = email.get('From', '').lower()

    content = ''
    if email.is_multipart():
        for part in email.get_payload():
            if part.get_content_type() in ['text/plain', 'text/html']:
                payload = part.get_payload(decode=True)
                if payload is not None:
                    content += payload.decode().lower()
    else:
        payload = email.get_payload(decode=True)
        if payload is not None:
            content = payload.decode().lower()

    for filter in config['filters']:
        keywords = [kw.lower() for kw in filter['keywords']]
        applies_to = filter.get('applyTo', [])

        if 'From' in applies_to and any(kw in from_field for kw in keywords):
            return filter['folder']
        if 'Subject' in applies_to and any(kw in subject for kw in keywords):
            return filter['folder']
        if 'Content' in applies_to and any(kw in content for kw in keywords):
            return filter['folder']

    return 'Inbox'
