import sys
from PyQt6.QtWidgets import QApplication
from gui.wmm_gui import WMMGui


def main():
    app = QApplication(sys.argv)
    window = WMMGui()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()