import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 Test')
window.setGeometry(100, 100, 300, 200)
label = QLabel('If you can see this, PyQt5 is working!', parent=window)
label.move(50, 80)
window.show()
sys.exit(app.exec_())