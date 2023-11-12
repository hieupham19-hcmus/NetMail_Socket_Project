from email import message_from_string, policy
import glob
from email.parser import BytesParser
from email.message import *
import os


def read_mail_from_file(path):
    """
    Read an email from a file.

    Parameters:
    path (str): The path to the file.

    Returns:
    str: The contents of the file.
    """
    with open(path, 'r') as file:
        return file.read()

def remove_metadata(email_str):
    """Remove metadata from email response."""
    return '\n'.join(email_str.splitlines()[1:-1])

def print_email_with_attachment_check(email_str):
    """
    Prints the details of an email and checks for attachments.

    Parameters:
    email_str (str): A string representation of the email.

    Returns:
    bool: True if the email has attachments, False otherwise.
    """

    email = message_from_string(email_str, policy=policy.default)
    # Extracting email details
    from_address = email['From']
    to_address = email["To"]
    subject = email["Subject"]

    print(f'From: {from_address}')
    print(f'To: {to_address}')
    print(f'Subject: {subject}')

    has_attachments = False

    # Function to print and check each part of the email
    def process_part(part):
        nonlocal has_attachments
        content_disposition = str(part.get("Content-Disposition", ""))
        if "attachment" in content_disposition:
            has_attachments = True
        else:
            payload = part.get_payload(decode=True).decode()
            print(f'Content: {payload}')

    # Process each part of the email
    if email.is_multipart():
        for part in email.iter_parts():
            process_part(part)
    else:
        process_part(email)

    print('-----------------------------')
    return has_attachments


def list_emails_in_folder(folder):
    folder_path = os.path.join(os.getcwd(), folder)
    
    if not os.path.exists(folder_path):
        print(f"Lỗi: Thư mục '{folder}' không tồn tại.")
        return

    search_pattern = os.path.join(folder_path, '*.eml')
    email_list = glob.glob(search_pattern, recursive=True)

    if not email_list:
        print(f"Không có email nào trong thư mục '{folder}'.")
        return

    print(f"Đây là danh sách email trong thư mục '{folder}':")
    for i, eml_file in enumerate(email_list, start=1):
        try:
            with open(eml_file, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)
                sender = msg.get('From')
                subject = msg.get('Subject')
                print(f"{i}. {sender}, {subject}")
        except Exception as e:
            print(f"Không thể đọc email {eml_file}: {e}")

def save_attachment(attachments, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename, content in attachments.items():
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Attachment '{filename}' saved to '{directory}'.")

def pick_mail_in_folder(folder, index):
    folder_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(folder_path):
        print(f"Lỗi: Thư mục '{folder}' không tồn tại.")
        return None, None

    email_files = glob.glob(os.path.join(folder_path, '*.eml'))
    if not email_files:
        print(f"Không có email nào trong thư mục '{folder}'.")
        return None, None

    if index > len(email_files):
        print(f"Không có email nào có số thứ tự {index} trong thư mục '{folder}'.")
        return None, None

    try:
        with open(email_files[index - 1], 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        attachments = {}
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') and "attachment" in part['Content-Disposition']:
                filename = part.get_filename()
                attachments[filename] = part.get_payload(decode=True)

        return msg, attachments

    except Exception as e:
        print(f"Không thể đọc email {email_files[index]}: {e}")
        return None, None


