import sys
import requests
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtWidgets import ( QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDialog, QFormLayout, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QFont, QPalette, QColor, QImage, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
import os
os.environ['ALL_PROXY']='http://127.0.0.1:7890'
class ChatWindow(QWidget):
    def __init__(self,apikey):
        super().__init__()

        self.init_ui()
        self.apikey = apikey
        self.messages = []

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
            self.messages.append({"role": "user", "content": user_message})
            response = self.get_api_response(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            self.messages=self.messages[-6:]
            self.conversation_area.append(f"Bot: {response}")
            self.input_line.clear()

    def get_api_response(self, messages):
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.apikey}","Content-Type": "application/json"}
        payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages
        }
        response = requests.post(api_url, json=payload,headers=headers)
        Hjson = json.loads(response.text)
        if response.status_code == 200:
            return Hjson["choices"][0]["message"]["content"]
        else:
            return "Sorry, something went wrong with the API request."
    
    def search_wikipedia(self):
        user_message = self.input_line.text()
        api_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "formatversion": 2,
            "srsearch": user_message,
            "srlimit": 10,
            "srprop": "snippet"
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            search_results = data["query"]["search"]
            selected_page = self.show_search_results(search_results)
            if selected_page:
                self.show_wikipedia_page(selected_page)
        else:
            self.conversation_area.append("Bot: Sorry, I couldn't find any results.")
        self.input_line.clear()

    def show_search_results(self, search_results):
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle("Search Results")

        layout = QVBoxLayout()

        result_list = QListWidget()
        for item in search_results:
            result_item = QListWidgetItem(item["title"])
            result_item.setData(Qt.UserRole, item["pageid"])
            result_list.addItem(result_item)
        layout.addWidget(result_list)

        select_button = QPushButton("Select")
        select_button.clicked.connect(result_dialog.accept)
        layout.addWidget(select_button)
        result_dialog.setLayout(layout)
        if result_dialog.exec_() == QDialog.Accepted:
            selected_item = result_list.currentItem()
        if selected_item:
            pageid = selected_item.data(Qt.UserRole)
            title = selected_item.text()
            return {"pageid": pageid, "title": title}
        return None

    def show_wikipedia_page(self, selected_page):
        page_dialog = QDialog(self)
        page_dialog.setWindowTitle(selected_page["title"])

        layout = QVBoxLayout()

        web_view = QWebEngineView()
        url = f"https://en.wikipedia.org/?curid={selected_page['pageid']}"
        web_view.load(QUrl(url))
        layout.addWidget(web_view)

        page_dialog.setLayout(layout)
        page_dialog.setFixedSize(800, 600)
        page_dialog.exec_()

    def get_image_from_api(self):
        user_message = self.input_line.text()
        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {self.apikey}","Content-Type": "application/json"}
        json ={
            "prompt": user_message,
            "n": 1,
            "size": "256x256"
        }
        response = requests.post(url, headers=headers,json=json)
        if response.status_code == 200:
            image_url=response.json()["data"][0]
            if image_url:
                    self.show_image(image_url["url"])
        else:
            self.conversation_area.append("Bot: Sorry, I couldn't find any image.")
        self.input_line.clear()

    def show_image(self, image_url):
        image_dialog = QDialog(self)
        image_dialog.setWindowTitle("Generated Image")

        layout = QVBoxLayout()

        image_label = QLabel()
        image_data = requests.get(image_url).content
        image = QImage()
        image.loadFromData(image_data)
        pixmap = QPixmap(image)
        image_label.setPixmap(pixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout.addWidget(image_label)

        image_dialog.setLayout(layout)
        image_dialog.setFixedSize(640, 480)
        image_dialog.exec_()

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
        test_api_url = "https://api.openai.com/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(test_api_url, headers=headers)

        return response.status_code == 200

