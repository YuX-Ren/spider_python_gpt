from PyQt5.QtWidgets import QApplication,QDialog
import sys
from interface import LoginWindow,ChatWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()

    if login_window.exec_() == QDialog.Accepted:
        # If the login is successful, show the chat window
        api_key = login_window.api_key_input.text()
        chat_window = ChatWindow(api_key)
        chat_window.show()
        sys.exit(app.exec_())
    sys.exit()