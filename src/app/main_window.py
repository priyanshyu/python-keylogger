import sys
import os

# Add the src directory to the path so ai_integration can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QThread, QObject
from ai_integration.analyzer_service import AIAnalyzer
from keylogger.keyboard_logger import KeyboardLogger
from keylogger.mouse_logger import MouseLogger

class KeyloggerWorker(QObject):
    def run(self):
        logger = KeyboardLogger()
        logger.run_listener()

class MouseLoggerWorker(QObject):
    def run(self):
        logger = MouseLogger()
        logger.start_periodic_save()  # Optional periodic save
        logger.run()

class KeyloggerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Keylogger App")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)

        self.keylogger_button = QPushButton('Start Keylogger', self)
        self.mouse_logger_button = QPushButton('Start Mouse Logger', self)
        self.ai_button = QPushButton('Analyze Logs with AI', self)
        self.exit_button = QPushButton('Exit', self)

        layout.addWidget(self.keylogger_button)
        layout.addWidget(self.mouse_logger_button)
        layout.addWidget(self.ai_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.log_display)

        self.setLayout(layout)

        self.keylogger_button.clicked.connect(self.start_keylogger)
        self.mouse_logger_button.clicked.connect(self.start_mouse_logger)
        self.ai_button.clicked.connect(self.analyze_logs)
        self.exit_button.clicked.connect(self.close_app)

    def start_keylogger(self):
        self.log_display.append("Starting Keylogger...")
        self.keylogger_thread = QThread()
        self.keylogger_worker = KeyloggerWorker()
        self.keylogger_worker.moveToThread(self.keylogger_thread)
        self.keylogger_thread.started.connect(self.keylogger_worker.run)
        self.keylogger_thread.start()

    def start_mouse_logger(self):
        self.log_display.append("Starting Mouse Logger...")
        self.mouse_logger_thread = QThread()
        self.mouse_logger_worker = MouseLoggerWorker()
        self.mouse_logger_worker.moveToThread(self.mouse_logger_thread)
        self.mouse_logger_thread.started.connect(self.mouse_logger_worker.run)
        self.mouse_logger_thread.start()

    def analyze_logs(self):
        self.log_display.append("Analyzing logs with AI...")
         
        analyzer = AIAnalyzer("keylogs.json", "mouse_logs.json")
        result = analyzer.analyze()
        self.log_display.append(f"AI Analysis Result:\n{result}")

    def close_app(self):
        self.log_display.append("Exiting application...")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyloggerApp()
    window.show()
    sys.exit(app.exec_())
