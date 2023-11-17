from email import message_from_string, policy
import glob
from email.parser import BytesParser
from email.message import *
import os
import sqlite3


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


def print_email_details(email):
    """
    Prints the details of an email.

    Parameters:
    email_str (str): A string representation of the email.
    """

    # Extracting email details
    print('-----------------------------')

    from_address = email['From']
    print(f'From: {from_address}')

    if email.get('To'):
        to_address = email.get('To')
        print(f'To: {to_address}')

    if email.get('CC'):
        cc_address = email.get('CC')
        print(f'CC: {cc_address}')

    if email.get('BCC'):
        bcc_address = email.get('BCC')
        print(f'BCC: {bcc_address}')

    date = email.get('Date', 'N/A')
    print(f'Date: {date}')

    subject = email.get('Subject', 'N/A')
    print(f'Subject: {subject}')

    # Function to process and print text parts of the email
    def process_part(part):
        if part.get_content_type() == 'text/plain':
            payload = part.get_payload(decode=True).decode()
            print(f'Content: {payload}')

    # Process each part of the email
    if email.is_multipart():
        for part in email.iter_parts():
            process_part(part)
    else:
        process_part(email)

    print('-----------------------------')


"""
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
"""


def list_emails_in_folder(folder):
    folder_path = os.path.join(os.getcwd(), 'Email\\' + folder)

    if not os.path.exists(folder_path):
        print(f"Lỗi: Thư mục '{folder}' không tồn tại.")
        return

    search_pattern = os.path.join(folder_path, '*.eml')
    email_list = glob.glob(search_pattern, recursive=True)

    if not email_list:
        print(f"Không có email nào trong thư mục '{folder}'.")
        return

    # Connect to the database
    conn = sqlite3.connect('database.sqlite')  # Replace with your database file
    cursor = conn.cursor()

    print(f"Đây là danh sách email trong thư mục '{folder}':")
    for i, eml_file in enumerate(email_list, start=1):
        try:
            with open(eml_file, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)
                sender = msg.get('From')
                subject = msg.get('Subject')
                # Extract message_id from file name or another source
                message_id = msg.get('Message-ID')  # Replace this with actual extraction logic

                # Fetch the status from the database
                cursor.execute("SELECT status FROM message_status WHERE message_id = ?", (message_id,))
                result = cursor.fetchone()
                status = result[0] if result else 1  # Default to 1 (unread) if not found in database

                # Add (chưa đọc) for unread emails
                unread_tag = "(chưa đọc) " if status == 0 else ""
                print(f"{i}. {unread_tag}{sender}, {subject}")
        except Exception as e:
            print(f"Không thể đọc email {eml_file}: {e}")

    # Close the database connection
    conn.close()


def save_attachment(attachments, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for filename, content in attachments.items():
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Attachment '{filename}' saved to '{directory}'.")


def pick_mail_in_folder(folder, index):
    folder_path = os.path.join(os.getcwd(), 'Email\\' + folder)
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

        # Extract message_id from file name or another source
        message_id = msg.get('Message-ID')  # Replace this with actual extraction logic

        # Update the status in the database
        conn = sqlite3.connect('database.sqlite')  # Replace with your database file
        cursor = conn.cursor()
        cursor.execute("UPDATE message_status SET status = 1 WHERE message_id = ?", (message_id,))
        conn.commit()
        conn.close()

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


"""
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

"""
