import logging
import signal
import sys

import requests

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BACKEND_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)s | GUI | %(message)s"
)

logger = logging.getLogger(__name__)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        logger.debug("Creating MainWindow")
        self.selected_message_id = None

        self.setWindowTitle("🐳 Docker Learning App")
        self.resize(600, 450)

        self.create_widgets()
        self.create_layout()
        self.connect_signals()

        logger.debug("MainWindow initialization completed")

        # Load messages after the Qt event loop starts.
        QTimer.singleShot(0, self.get_messages)

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def create_widgets(self):
        logger.debug("Creating GUI widgets")

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter message...")

        self.get_button = QPushButton("📥 GET")
        self.create_button = QPushButton("➕ CREATE")
        self.update_button = QPushButton("✏️ UPDATE")
        self.delete_button = QPushButton("🗑️ DELETE")

        self.messages_list = QListWidget()
        self.status_label = QLabel("Ready")

    def create_layout(self):
        logger.debug("Creating GUI layout")

        title = QLabel("🐳 Docker Learning App")
        message_label = QLabel("Message:")
        messages_label = QLabel("📋 All Messages:")

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.get_button)
        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(message_label)
        layout.addWidget(self.message_input)
        layout.addLayout(buttons_layout)
        layout.addWidget(messages_label)
        layout.addWidget(self.messages_list)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def connect_signals(self):
        logger.debug("Connecting GUI signals")
        self.get_button.clicked.connect(self.get_messages)
        self.create_button.clicked.connect(self.create_message)
        self.update_button.clicked.connect(self.update_message)
        self.delete_button.clicked.connect(self.delete_message)
        self.messages_list.itemClicked.connect(self.select_message)

    # --------------------------------------------------
    # GET
    # --------------------------------------------------

    def get_messages(self):
        logger.debug("GET /messages - sending request")
        try:
            response = requests.get(f"{BACKEND_URL}/messages", timeout=5)
            logger.debug("GET /messages - status=%s", response.status_code)
            response.raise_for_status()
            messages = response.json()
            logger.debug("GET /messages - received %d message(s)", len(messages))
            self.messages_list.clear()
            for message in messages:
                logger.debug("Displaying message id=%s", message["id"])
                self.messages_list.addItem(
                    f"{message['id']} | " f"{message['message']}"
                )
            self.status_label.setText(f"✅ Loaded {len(messages)} message(s)")

        except requests.RequestException:
            logger.exception("GET /messages failed")
            self.show_error(
                "Unable to get messages.\n" "Make sure the backend is running."
            )

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------

    def create_message(self):
        message = self.message_input.text().strip()
        logger.debug("CREATE requested: message=%r", message)
        if not message:
            logger.warning("CREATE rejected: empty message")
            self.show_error("Please enter a message.")
            return

        try:
            logger.debug("POST /messages - sending request")
            response = requests.post(
                f"{BACKEND_URL}/messages", json={"message": message}, timeout=5
            )
            logger.debug("POST /messages - status=%s", response.status_code)
            response.raise_for_status()
            created = response.json()
            logger.info("Message created: id=%s", created["id"])
            self.message_input.clear()
            self.status_label.setText("✅ Message created")
            self.get_messages()

        except requests.RequestException:
            logger.exception("POST /messages failed")
            self.show_error("Unable to create message.")

    # --------------------------------------------------
    # SELECT
    # --------------------------------------------------

    def select_message(self, item):
        logger.debug("Message selected: %s", item.text())
        message_id, message = item.text().split(" | ", 1)
        self.selected_message_id = int(message_id)
        self.message_input.setText(message)
        self.status_label.setText(f"Selected message #{message_id}")

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update_message(self):
        logger.debug("UPDATE requested for id=%s", self.selected_message_id)
        if self.selected_message_id is None:
            logger.warning("UPDATE rejected: no message selected")
            self.show_error("Please select a message first.")
            return

        message = self.message_input.text().strip()
        if not message:
            logger.warning("UPDATE rejected: empty message")
            self.show_error("Please enter a message.")
            return

        try:
            logger.debug("PUT /messages/%s - sending request", self.selected_message_id)
            response = requests.put(
                f"{BACKEND_URL}/messages/" f"{self.selected_message_id}",
                json={"message": message},
                timeout=5,
            )
            logger.debug(
                "PUT /messages/%s - status=%s",
                self.selected_message_id,
                response.status_code,
            )
            response.raise_for_status()
            logger.info("Message updated: id=%s", self.selected_message_id)
            self.message_input.clear()
            self.selected_message_id = None
            self.status_label.setText("✅ Message updated")
            self.get_messages()

        except requests.RequestException:
            logger.exception("PUT /messages/%s failed", self.selected_message_id)
            self.show_error("Unable to update message.")

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------

    def delete_message(self):
        logger.debug("DELETE requested for id=%s", self.selected_message_id)
        if self.selected_message_id is None:
            logger.warning("DELETE rejected: no message selected")
            self.show_error("Please select a message first.")
            return

        try:
            logger.debug(
                "DELETE /messages/%s - sending request", self.selected_message_id
            )
            response = requests.delete(
                f"{BACKEND_URL}/messages/" f"{self.selected_message_id}", timeout=5
            )
            logger.debug(
                "DELETE /messages/%s - status=%s",
                self.selected_message_id,
                response.status_code,
            )
            response.raise_for_status()
            logger.info("Message deleted: id=%s", self.selected_message_id)
            self.message_input.clear()
            self.selected_message_id = None
            self.status_label.setText("✅ Message deleted")
            self.get_messages()

        except requests.RequestException:
            logger.exception("DELETE /messages failed")
            self.show_error("Unable to delete message.")

    # --------------------------------------------------
    # ERROR
    # --------------------------------------------------

    def show_error(self, message):
        logger.error("GUI error: %s", message)
        self.status_label.setText("❌ Operation failed")
        QMessageBox.critical(self, "Error", message)


# --------------------------------------------------
# Ctrl+C handling
# --------------------------------------------------


def handle_sigint(*_):
    logger.info("Ctrl+C received - terminating GUI")
    QApplication.quit()


def main():
    logger.info("Starting Docker Learning App GUI")
    # Allow Ctrl+C to reach Python while
    # Qt's event loop is running.
    signal.signal(signal.SIGINT, handle_sigint)
    application = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    logger.info("GUI event loop starting")
    exit_code = application.exec()
    logger.info("GUI terminated with exit code=%s", exit_code)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
