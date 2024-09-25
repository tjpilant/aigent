import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QCoreApplication

class AIGentGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AIGent: Intelligent Document Processor")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

def main():
    # Set the platform to "offscreen" if no display is available
    if not QCoreApplication.instance():
        QCoreApplication.setAttribute(QCoreApplication.AA_UseSoftwareOpenGL)
        QApplication.setStyle('Fusion')

    app = QApplication(sys.argv)
    
    # Check if a screen is available
    if not app.primaryScreen():
        print("No screen detected. Running in headless mode.")
        return

    ex = AIGentGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()