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

def save_attachment(filenames, directory, attachments):
    """
    Save specified attachments to a given directory.

    :param filenames: List of filenames to be saved.
    :param directory: The directory where files will be saved.
    :param attachments: Dictionary containing attachments with filenames as keys and content as values.
    """
    import os

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Iterate over the filenames
    for filename in filenames:
        if filename in attachments:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'wb') as file:
                file.write(attachments[filename])
            print(f"Attachment '{filename}' saved to '{directory}'.")
        else:
            print(f"Attachment '{filename}' not found in the attachments.")

def pick_mail_in_folder(folder, index):
    folder_path = os.path.join(os.getcwd(), folder)

    if not os.path.exists(folder_path):
        print(f"Lỗi: Thư mục '{folder}' không tồn tại.")
        return None, False

    search_pattern = os.path.join(folder_path, '*.eml')
    email_list = glob.glob(search_pattern, recursive=True)

    if not email_list:
        print(f"Không có email nào trong thư mục '{folder}'.")
        return None, False

    if index > len(email_list):
        print(f"Không có email nào có số thứ tự {index} trong thư mục '{folder}'.")
        return None, False

    attachment_filenames = []
    has_attachment = False
    msg = None
    try:
        with open(email_list[index-1], 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
            print(f"From: {msg.get('From')}")
            print(f"To: {msg.get('To')}")
            if msg.get('Cc'):
                print(f"Cc: {msg.get('Cc')}")
            if msg.get('Bcc'):
                print(f"Bcc: {msg.get('Bcc')}")
            print(f"Subject: {msg.get('Subject')}")

            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                if "attachment" in content_disposition:
                    attachment_filenames.append(part.get_filename())
                    has_attachment = True
                elif content_type in ["text/plain", "text/html"]:
                    # Chỉ in nội dung văn bản
                    payload = part.get_payload(decode=True).decode()
                    #print(f"Content: {payload}")

    except Exception as e:
        print(f"Không thể đọc email {email_list[index-1]}: {e}")
        return None, False

    return attachment_filenames, has_attachment


