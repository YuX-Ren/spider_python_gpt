import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QFrame, QDialog, QFormLayout
from PyQt5.QtGui import QFont, QPalette, QColor
import json
import os
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
class ChatWindow(QWidget):
    def __init__(self,apikey):
        super().__init__()

        self.init_ui()
        self.apikey = apikey

    def init_ui(self):
        self.setWindowTitle('Chat Interface')

        # Window size and styling
        self.setFixedSize(800, 600)
        self.setAutoFillBackground(True)

        p = self.palette()
        p.setColor(QPalette.Background, QColor(240, 240, 240))
        self.setPalette(p)

        # Set layout
        layout = QVBoxLayout()

        # Add header
        header = QLabel('Chat with Bot')
        header_font = QFont('Arial', 24, QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Add text area for the conversation
        self.conversation_area = QTextEdit()
        self.conversation_area.setReadOnly(True)
        layout.addWidget(self.conversation_area)

        # Add input container
        input_container = QHBoxLayout()

        # Add input field
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('Type your message here...')
        self.input_line.setFixedHeight(40)
        input_container.addWidget(self.input_line)

        # Add input container to the main layout
        layout.addLayout(input_container)

        # Add buttons
        buttons = QHBoxLayout()
        
        # Add send button
        send_button = QPushButton('chat')
        send_button.setFixedHeight(40)
        send_button.clicked.connect(self.send_message)
        buttons.addWidget(send_button)

        # Add search_wiki button
        send_button = QPushButton('search_wiki')
        send_button.setFixedHeight(40)
        send_button.clicked.connect(self.search_wikipedia)
        buttons.addWidget(send_button)

        # Add image button
        send_button = QPushButton('image_generation')
        send_button.setFixedHeight(40)
        send_button.clicked.connect(self.get_image_from_api)
        buttons.addWidget(send_button)

        # Add buttons to the main layout
        layout.addLayout(buttons)

        # Add horizontal line separator
        hline = QFrame()
        hline.setFrameShape(QFrame.HLine)
        hline.setFrameShadow(QFrame.Sunken)
        layout.addWidget(hline)

        self.setLayout(layout)

    def send_message(self):
        user_message = self.input_line.text()
        if user_message:
            self.conversation_area.append(f"You: {user_message}")
            response = self.get_api_response(user_message)
            self.conversation_area.append(f"Bot: {response}")
            self.input_line.clear()

    def get_api_response(self, message):
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.apikey}","Content-Type": "application/json"}
        payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(api_url, json=payload,headers=headers)
        print(response.text)
        Hjson = json.loads(response.text)
        if response.status_code == 200:
            return Hjson["choices"][0]["message"]["content"]
        else:
            return "Sorry, something went wrong with the API request."
    
    def search_wikipedia(self):
        pass

    def get_image_from_api(self):
        pass

# Add a LoginWindow class
class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("API Key Login")

        layout = QFormLayout()

        self.api_key_input = QLineEdit()
        layout.addRow("API Key:", self.api_key_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.check_api_key)
        layout.addRow(login_button)

        self.setLayout(layout)

    def check_api_key(self):
        api_key = self.api_key_input.text()
        if self.verify_api_key(api_key):
            self.accept()
        else:
            self.api_key_input.clear()
            self.api_key_input.setPlaceholderText("Invalid API key, please try again")

    def verify_api_key(self, api_key):
        # Replace this function with a request to your API that checks the validity of the provided API key
        test_api_url = "https://your-api-url.com/verify"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(test_api_url, headers=headers)

        return response.status_code == 200



if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()

    if login_window.exec_() == QDialog.Accepted:
        # If the login is successful, show the chat window
        api_key = login_window.api_key_input.text()
        chat_window = ChatWindow(api_key)
        chat_window.show()
        sys.exit(app.exec_())
    sys.exit(app.exec_())
