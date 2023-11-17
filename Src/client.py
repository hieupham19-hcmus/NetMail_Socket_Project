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


def main():
    config = read_config_file('config.json')
    smtp_port = int(config['SMTP'])
    pop3_port = int(config['POP3'])
    userPassword = config['Password']
    host = config['MailServer']
    userEmail = config['Email']
    userName = config['Username']
    autoLoad = int(config['AutoLoad'])

    auto_run_function(autoLoad, receive_email, host, pop3_port, userEmail, userPassword)

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
                receive_email(host, pop3_port, userEmail, userPassword)
                print("Đây là danh sách các folder trong mailbox của bạn:")
                print("1. Inbox")
                print("2. Project")
                print("3. Important")
                print("4. Work")
                print("5. Spam")
                choice_folder = input("Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ")

                if choice_folder == '1':
                    os.system("cls")
                    list_emails_in_folder('Inbox')
                    choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")
                    if choice_mail == '':
                        break
                    else:
                        msg, attachments = pick_mail_in_folder('Inbox', int(choice_mail))
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input(
                                "Trong email này có attached file, bạn có muốn save không (1. có, 2. không): ")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    pass
                elif choice_folder == '2':
                    clear_screen()
                    list_emails_in_folder('Project')
                    choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")
                    if choice_mail == '':
                        break
                    else:
                        msg, attachments = pick_mail_in_folder('Project', int(choice_mail))
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input(
                                "Trong email này có attached file, bạn có muốn save không (1. có, 2. không):")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    pass
                elif choice_folder == '3':
                    clear_screen()
                    list_emails_in_folder('Important')
                    choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")
                    if choice_mail == '':
                        break
                    else:
                        msg, attachments = pick_mail_in_folder('Important', int(choice_mail))
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input(
                                "Trong email này có attached file, bạn có muốn save không (1. có, 2. không):")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    pass
                elif choice_folder == '4':
                    clear_screen()
                    list_emails_in_folder('Work')
                    choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")
                    if choice_mail == '':
                        break
                    else:
                        msg, attachments = pick_mail_in_folder('Work', int(choice_mail))
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input(
                                "Trong email này có attached file, bạn có muốn save không (1. có, 2. không):")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    pass
                elif choice_folder == '5':
                    clear_screen()
                    list_emails_in_folder('Spam')
                    choice_mail = input("Bạn muốn xem email nào (Nhấn enter để thoát ra ngoài): ")
                    if choice_mail == '':
                        break
                    else:
                        msg, attachments = pick_mail_in_folder('Spam', int(choice_mail))
                        print_email_details(msg)
                        if attachments:
                            choice_tmp = input(
                                "Trong email này có attached file, bạn có muốn save không (1. có, 2. không):")
                            if choice_tmp == '1':
                                path = input("Nhập đường dẫn để save file: ")
                                save_attachment(attachments, path)
                        wait_for_enter()
                    pass
                elif choice_folder == '':
                    break
                else:
                    print("Tùy chọn không hợp lệ. Vui lòng chọn lại.")
            pass
        elif choice == '3':
            sys.exit()
        else:
            print("Tùy chọn không hợp lệ. Vui lòng chọn lại.")


if __name__ == '__main__':
    main()
