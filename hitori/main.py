import sys
from PyQt5.QtWidgets import QApplication
from hitori import window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    field = window.Window()
    sys.exit(app.exec_())
