print("Initializing AIGentGUI")
from aigent import ai_service
from aigent import api_manager
from aigent import file_converter
from aigent import image_converter
from aigent import aigent_gui
print("AIGentGUI initialized")

if __name__ == "__main__":
    print("Starting main")
    app = QApplication(sys.argv)
    print("QApplication created")
    ex = AIGentGUI()
    print("AIGentGUI instance created")
    ex.show()
    print("show() called on AIGentGUI instance")
    sys.exit(app.exec_())
