from EmailProcessor import *
from Receive_Email import *
from Send_Email import send_email
from readConfig import read_config_file
import subprocess
import threading
import sys


def clear_screen():
    """Clears the terminal no matter what OS you're using"""
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)


def wait_for_enter():
    while True:
        response = input("Nhấn Enter để quay lại menu chính... ")
        if response == "":
            break


def auto_run_function(interval, func, *args):
    threading.Timer(interval, auto_run_function, [interval, func] + list(args)).start()
    func(*args)

def get_existing_mail_folders():
    mailbox_path = os.path.join(os.getcwd(), 'Email')
    if not os.path.exists(mailbox_path):
        print("Mailbox directory not found.")
        return []

    folders = next(os.walk(mailbox_path))[1]  # List of folder names in the mailbox directory
    return folders

def main():
    config = read_config_file('config.json')
    smtp_port = int(config['general']['SMTP'])
    pop3_port = int(config['general']['POP3'])
    userPassword = config['general']['Password']
    host = config['general']['MailServer']
    userEmail = config['general']['Email']
    userName = config['general']['Username']
    autoLoad = int(config['general']['AutoLoad'])

    auto_run_function(autoLoad, receive_email, host, pop3_port, userEmail, userPassword, config)

    while True:
        clear_screen()
        print("Vui lòng chọn Menu:")
        print("1. Để gửi email")
        print("2. Để xem danh sách các email đã nhận")
        print("3. Thoát")
        choice = input("Bạn chọn: ")

        if choice == '1':
            clear_screen()
            print("Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)")
            to = input("To: ")
            cc = input("CC: ")
            bcc = input("BCC: ")
            userSubject = input("Subject: ")
            userBody = input("Content: ")

            while True:
                sendAttachment = input("Có gửi kèm file (1. có, 2. không): ")
                if sendAttachment in ['1', '2']:
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng nhập 1 hoặc 2.")

            toEmails = [email.strip() for email in to.split(',')] if to else []
            ccEmails = [email.strip() for email in cc.split(',')] if cc else []
            bccEmails = [email.strip() for email in bcc.split(',')] if bcc else []

            attachmentFilePaths = []
            if sendAttachment == '1':
                attachmentCount = int(input('Số lượng file muốn gửi: '))
                for i in range(attachmentCount):
                    filePath = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
                    attachmentFilePaths.append(filePath)

            send_email(host, smtp_port, userName, userEmail, userSubject, userBody, toEmails, ccEmails, bccEmails,
                       attachmentFilePaths)
            wait_for_enter()
        elif choice == '2':
            while True:
                clear_screen()
                receive_email(host, pop3_port, userEmail, userPassword, config)
                existing_folders = get_existing_mail_folders()
                if not existing_folders:
                    print("Không có thư mục nào trong mailbox.")
                    wait_for_enter()
                    break

                print("Đây là danh sách các folder trong mailbox của bạn:")
                for idx, folder in enumerate(existing_folders, start=1):
                    print(f"{idx}. {folder}")

                choice_folder = input("Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ")

                if choice_folder == '':
                    break
                try:
                    selected_folder_index = int(choice_folder) - 1
                    selected_folder = existing_folders[selected_folder_index]
                except (IndexError, ValueError):
                    print("Tùy chọn không hợp lệ. Vui lòng chọn lại.")
                    continue

                clear_screen()
                list_emails_in_folder(selected_folder)
                choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")

                if choice_mail == '':
                    continue
                else:
                    try:
                        selected_email = int(choice_mail)
                        msg, attachments = pick_mail_in_folder(selected_folder, selected_email)
                        os.system("cls")
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input("Trong email này có attached file, bạn có muốn save không (1. có, "
                                               "2. không): ")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    except ValueError:
                        print("Tùy chọn không hợp lệ. Vui lòng nhập một số.")
                    except Exception as e:
                        print(f"Có lỗi xảy ra: {e}")
        elif choice == '3':
            sys.exit()
        else:
            print("Tùy chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == '__main__':
    main()
