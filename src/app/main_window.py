import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QThread, QObject, pyqtSignal

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_integration.analyzer_service import AIAnalyzer
from keylogger.keyboard_logger import KeyboardLogger
from keylogger.mouse_logger import MouseLogger


class KeyloggerWorker(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logger = KeyboardLogger()
    
    def run(self):
        self.logger.start_listener()

    def stop(self):
        self.logger.stop_listener()
        self.finished.emit()


class MouseLoggerWorker(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.logger = MouseLogger()
    
    def run(self):
        self.logger.start_listener()
        self.logger.start_periodic_save()

    def stop(self):
        self.logger.stop_listener()
        self.finished.emit()


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

        self.keylogger_running = False
        self.mouse_logger_running = False

        self.keylogger_thread = None
        self.mouse_logger_thread = None
        self.keylogger_worker = None
        self.mouse_logger_worker = None

        self.keylogger_button.clicked.connect(self.toggle_keylogger)
        self.mouse_logger_button.clicked.connect(self.toggle_mouse_logger)
        self.ai_button.clicked.connect(self.analyze_logs)
        self.exit_button.clicked.connect(self.close_app)

    def toggle_keylogger(self):
        if not self.keylogger_running:
            self.log_display.append("Starting Keylogger...")
            self.keylogger_thread = QThread()
            self.keylogger_worker = KeyloggerWorker()
            self.keylogger_worker.moveToThread(self.keylogger_thread)
            self.keylogger_thread.started.connect(self.keylogger_worker.run)
            self.keylogger_worker.finished.connect(self.keylogger_thread.quit)
            self.keylogger_worker.finished.connect(self.keylogger_worker.deleteLater)
            self.keylogger_thread.finished.connect(self.keylogger_thread.deleteLater)
            self.keylogger_thread.start()
            self.keylogger_button.setText("Stop Keylogger")
            self.keylogger_running = True
        else:
            self.log_display.append("Stopping Keylogger...")
            if self.keylogger_worker:
                self.keylogger_worker.stop()
            self.keylogger_running = False
            self.keylogger_button.setText("Start Keylogger")

    def toggle_mouse_logger(self):
        if not self.mouse_logger_running:
            self.log_display.append("Starting Mouse Logger...")
            self.mouse_logger_thread = QThread()
            self.mouse_logger_worker = MouseLoggerWorker()
            self.mouse_logger_worker.moveToThread(self.mouse_logger_thread)
            self.mouse_logger_thread.started.connect(self.mouse_logger_worker.run)
            self.mouse_logger_worker.finished.connect(self.mouse_logger_thread.quit)
            self.mouse_logger_worker.finished.connect(self.mouse_logger_worker.deleteLater)
            self.mouse_logger_thread.finished.connect(self.mouse_logger_thread.deleteLater)
            self.mouse_logger_thread.start()
            self.mouse_logger_button.setText("Stop Mouse Logger")
            self.mouse_logger_running = True
        else:
            self.log_display.append("Stopping Mouse Logger...")
            if self.mouse_logger_worker:
                self.mouse_logger_worker.stop()
            self.mouse_logger_running = False
            self.mouse_logger_button.setText("Start Mouse Logger")

    def analyze_logs(self):
        self.log_display.append("Analyzing logs with AI...")
        analyzer = AIAnalyzer("keylogs.json", "mouse_logs.json")
        result = analyzer.analyze()
        self.log_display.append(f"AI Analysis Result:\n{result}")

    def close_app(self):
        self.log_display.append("Exiting application...")
        if self.keylogger_worker and self.keylogger_running:
            self.keylogger_worker.stop()
        if self.mouse_logger_worker and self.mouse_logger_running:
            self.mouse_logger_worker.stop()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyloggerApp()
    window.show()
    sys.exit(app.exec_())
