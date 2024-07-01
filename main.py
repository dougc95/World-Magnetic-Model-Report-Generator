import sys
from PyQt6.QtWidgets import QApplication
from gui.wmm_gui import WMMGui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WMMGui()
    gui.setWindowTitle('WMM Excel Generator')
    gui.resize(800, 300)
    gui.show()
    sys.exit(app.exec())