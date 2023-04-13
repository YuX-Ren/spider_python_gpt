import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QFrame
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

        # Add input and send button container
        input_container = QHBoxLayout()

        # Add input field
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText('Type your message here...')
        self.input_line.setFixedHeight(40)
        input_container.addWidget(self.input_line)

        # Add send button
        send_button = QPushButton('Send')
        send_button.setFixedHeight(40)
        send_button.clicked.connect(self.send_message)
        input_container.addWidget(send_button)

        # Add input container to the main layout
        layout.addLayout(input_container)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apikey = " "
    chat_window = ChatWindow(apikey)
    chat_window.show()

    sys.exit(app.exec_())
